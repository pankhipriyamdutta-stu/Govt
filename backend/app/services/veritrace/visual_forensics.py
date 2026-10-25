import os
import tempfile
from typing import Dict, Any, List, Optional
import numpy as np

class VisualForensicsService:
    @staticmethod
    def is_opencv_available() -> bool:
        try:
            import cv2
            return True
        except ImportError:
            return False

    @classmethod
    def analyze_image_tampering(cls, image_path: str, quality: int = 90) -> Dict[str, Any]:
        """
        Conducts Digital Image Forensics using OpenCV:
        1. Error Level Analysis (ELA): Computes compression disparity to detect pasted / altered blocks.
        2. Blur / Sharpness Variance: Uses Laplacian operator to detect spliced digital text on scanned paper.
        3. Local Noise Uniformity: Examines grid-level variance to detect altered signatures or stamps.
        4. Suspicious region extraction with bounding coordinates.
        Does NOT modify the original image file.
        """
        if not os.path.exists(image_path):
            return {
                "evaluated": False,
                "error": "Image file not found",
                "visual_tampering_score": 0.0,
                "verdict": "NOT_EVALUATED",
                "suspicious_regions": [],
                "ela_mean_error": 0.0,
                "sharpness_variance": 0.0,
                "summary": "Visual analysis could not be conducted because target image was not found."
            }

        try:
            import cv2

            img = cv2.imread(image_path)
            if img is None:
                return {
                    "evaluated": False,
                    "error": "Failed to decode image bytes with OpenCV",
                    "visual_tampering_score": 0.0,
                    "verdict": "DECODE_FAILURE",
                    "suspicious_regions": [],
                    "summary": "OpenCV was unable to decode the image file."
                }

            h, w, c = img.shape

            # 1. Error Level Analysis (ELA)
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
                tmp_jpeg = tmp_file.name

            try:
                cv2.imwrite(tmp_jpeg, img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
                recompressed = cv2.imread(tmp_jpeg)
                
                # Difference between original and recompressed
                diff = cv2.absdiff(img, recompressed)
                diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                ela_mean = float(np.mean(diff_gray))
                ela_std = float(np.std(diff_gray))
                ela_max = float(np.max(diff_gray))
            finally:
                if os.path.exists(tmp_jpeg):
                    try:
                        os.remove(tmp_jpeg)
                    except Exception:
                        pass

            # 2. Laplacian Blur / Edge Sharpness Consistency
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            global_sharpness = float(laplacian.var())

            # 3. Grid-based Block Anomaly Detection
            grid_rows = 6
            grid_cols = 6
            cell_h = h // grid_rows
            cell_w = w // grid_cols

            suspicious_regions: List[Dict[str, Any]] = []
            cell_ela_means = []
            cell_sharpness = []

            for r in range(grid_rows):
                for c_idx in range(grid_cols):
                    y1 = r * cell_h
                    y2 = (r + 1) * cell_h if r < grid_rows - 1 else h
                    x1 = c_idx * cell_w
                    x2 = (c_idx + 1) * cell_w if c_idx < grid_cols - 1 else w

                    cell_diff = diff_gray[y1:y2, x1:x2]
                    cell_gray = gray[y1:y2, x1:x2]

                    c_ela = float(np.mean(cell_diff))
                    c_sharp = float(cv2.Laplacian(cell_gray, cv2.CV_64F).var())

                    cell_ela_means.append((r, c_idx, x1, y1, x2 - x1, y2 - y1, c_ela, c_sharp))
                    cell_sharpness.append(c_sharp)

            median_ela = float(np.median([item[6] for item in cell_ela_means])) or 1.0
            median_sharp = float(np.median(cell_sharpness)) or 1.0

            tamper_points = 0
            for r, c_idx, x, y, cw, ch, c_ela, c_sharp in cell_ela_means:
                ela_ratio = c_ela / median_ela if median_ela > 0 else 1.0
                sharp_ratio = c_sharp / median_sharp if median_sharp > 0 else 1.0

                # High localized ELA difference implies spliced/different compression layer
                if ela_ratio > 3.0 and c_ela > 8.0:
                    tamper_points += 2
                    suspicious_regions.append({
                        "x": x,
                        "y": y,
                        "width": cw,
                        "height": ch,
                        "anomaly_type": "INCONSISTENT_COMPRESSION_LAYER",
                        "severity": "high" if ela_ratio > 4.5 else "medium",
                        "description": f"Grid block ({r},{c_idx}) displays compression disparity {ela_ratio:.1f}x higher than median."
                    })
                elif sharp_ratio > 5.0 and c_sharp > 150.0 and global_sharpness < 50.0:
                    tamper_points += 1
                    suspicious_regions.append({
                        "x": x,
                        "y": y,
                        "width": cw,
                        "height": ch,
                        "anomaly_type": "HIGH_RESOLUTION_OVERLAY_IN_SCANNED_PAGE",
                        "severity": "medium",
                        "description": f"Disproportionate sharpness spike ({sharp_ratio:.1f}x) on low-resolution scanned background."
                    })

            # Calculate normalized visual tampering risk score (0.0 to 1.0)
            tampering_score = min(1.0, round(tamper_points * 0.18 + (0.25 if ela_max > 45 else 0.0), 3))

            if tampering_score >= 0.65:
                verdict = "HIGH_PROBABILITY_VISUAL_TAMPERING"
                summary = f"Detected {len(suspicious_regions)} suspicious regions showing localized compression disparity and splicing indicators."
            elif tampering_score >= 0.35:
                verdict = "SUSPICIOUS_IMAGE_COMPRESSION_VARIANCE"
                summary = f"Found {len(suspicious_regions)} localized variances. May represent digital editing, form field filling, or mixed-resolution scans."
            else:
                verdict = "NATURAL_COMPRESSION_CONSISTENT"
                summary = "Error Level Analysis and edge distribution are uniform across document grid. No visual splicing detected."

            return {
                "evaluated": True,
                "visual_tampering_score": tampering_score,
                "verdict": verdict,
                "ela_mean_error": round(ela_mean, 2),
                "ela_max_error": round(ela_max, 2),
                "global_sharpness_variance": round(global_sharpness, 2),
                "suspicious_regions": suspicious_regions[:8],
                "summary": summary,
                "limitations": [
                    "Repeated multi-generation photocopying can normalize compression artifacts.",
                    "High-quality lossless rasterizations may yield negligible ELA variance."
                ]
            }
        except Exception as e:
            return {
                "evaluated": False,
                "error": str(e),
                "visual_tampering_score": 0.0,
                "verdict": "ERROR_DURING_EVALUATION",
                "suspicious_regions": [],
                "summary": f"Visual forensics analysis encountered an exception: {str(e)}"
            }
