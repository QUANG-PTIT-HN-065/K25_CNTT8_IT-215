import logging
import time
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from router import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - RequestID: %(message)s",
)
logger = logging.getLogger("api_logger")

app = FastAPI(title="Secure Learning Resources API", version="1.0.0")

# CORS Middleware
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.middleware("http")
async def process_time_and_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start_time
    process_time_ms = f"{process_time * 1000:.2f}ms"

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = process_time_ms

    logger.info(
        f"{request_id} | {request.method} {request.url.path} | "
        f"Status: {response.status_code} | Time: {process_time_ms}"
    )

    return response


app.include_router(router)
