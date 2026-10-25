import time
from collections import defaultdict
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.config import settings

# In-memory sliding-window request counters
# IP -> list of timestamps
REQUEST_TIMESTAMPS = defaultdict(list)

class SovereignSecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    CERT-In and NIC (GIGW 3.0) Compliant Security Headers & Defense Middleware.
    Enforces HSTS, Anti-Clickjacking, CSP, Anti-MIME sniffing, and DoS rate-limiting.
    """
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "127.0.0.1"
        now = time.time()
        
        # 1. Rate Limiting Check
        window = 60.0  # 1 minute window
        recent_reqs = [t for t in REQUEST_TIMESTAMPS[client_ip] if now - t < window]
        recent_reqs.append(now)
        REQUEST_TIMESTAMPS[client_ip] = recent_reqs

        is_auth_route = request.url.path.endswith("/auth/login")
        max_allowed = (
            settings.RATE_LIMIT_LOGIN_MAX_PER_MINUTE
            if is_auth_route
            else settings.RATE_LIMIT_QUERY_MAX_PER_MINUTE * 2
        )

        if len(recent_reqs) > max_allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "RATE_LIMIT_EXCEEDED",
                    "detail": "Automated brute-force or DoS threshold exceeded. Request blocked under CERT-In guidelines.",
                    "client_ip": client_ip,
                    "retry_after_seconds": 60
                },
                headers={"Retry-After": "60"}
            )

        # 2. Process Request
        response: Response = await call_next(request)

        # 3. Inject Sovereign Government Security Headers
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=(), payment=()"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "connect-src 'self' ws: http://localhost:* http://127.0.0.1:*; "
            "object-src 'none'; "
            "frame-ancestors 'none';"
        )
        response.headers["X-Govt-Security-Zone"] = "RESTRICTED-SOVEREIGN-SECURE"
        response.headers["X-Audit-Compliance"] = "CERT-In Section 70B & DPDP Act 2023"

        return response
