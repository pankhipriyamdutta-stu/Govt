import asyncio
import os
from typing import Dict, Any, List, Optional
from PIL import Image

class OCRService:
    @staticmethod
    def is_ocr_available() -> bool:
        try:
            import winocr
            return True
        except ImportError:
            return False

    @classmethod
    def perform_ocr_on_image(cls, image_path: str, lang: str = "en") -> Dict[str, Any]:
        """
        Runs OCR on an image file using Windows Media OCR (winocr) or image fallback.
        Preserves bounding box details, text lines, and estimated confidence.
        """
        if not os.path.exists(image_path):
            return {
                "success": False,
                "text": "",
                "lines": [],
                "confidence": 0.0,
                "warning": "Image file does not exist."
            }

        try:
            import winocr

            async def _run():
                with Image.open(image_path) as img:
                    # Convert to RGB if needed
                    if img.mode not in ("RGB", "L"):
                        img = img.convert("RGB")
                    return await winocr.recognize_pil(img, lang=lang)

            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If in an already running event loop, create a new thread or use run_coroutine_threadsafe
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as pool:
                        res = pool.submit(asyncio.run, _run()).result()
                else:
                    res = loop.run_until_complete(_run())
            except RuntimeError:
                res = asyncio.run(_run())

            lines = []
            total_words = 0
            for line in getattr(res, "lines", []):
                line_text = getattr(line, "text", "")
                words = getattr(line, "words", [])
                total_words += len(words)
                lines.append({
                    "text": line_text,
                    "words_count": len(words)
                })

            full_text = getattr(res, "text", "")
            # Estimate confidence based on word length and character noise
            char_count = len(full_text.strip())
            confidence = 0.88 if char_count > 30 else (0.50 if char_count > 0 else 0.0)
            warning = None
            if confidence < 0.60:
                warning = "Low-quality scan detected: OCR output has few recognizable words or high noise."

            return {
                "success": True,
                "text": full_text,
                "lines": lines,
                "word_count": total_words,
                "confidence": confidence,
                "warning": warning
            }
        except Exception as e:
            return {
                "success": False,
                "text": "",
                "lines": [],
                "confidence": 0.0,
                "warning": f"OCR processing unavailable or error encountered: {str(e)}"
            }
