import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.logger import get_logger
from app.routes import summarize, translate, generate_email

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION} (debug={settings.DEBUG})")
    yield
    logger.info(f"Shutting down {settings.APP_NAME}")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered REST API providing text summarization, translation, and email generation via Groq.",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
    },
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("→ %s %s | client: %s", request.method, request.url.path, request.client.host)
    start_time = time.time()
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000
    logger.info("← %d %s %s | %.2fms", response.status_code, request.method, request.url.path, duration)
    return response


app.include_router(summarize.router, prefix="/api/v1")
app.include_router(translate.router, prefix="/api/v1")
app.include_router(generate_email.router, prefix="/api/v1")


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception on %s %s: %s", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.get("/", tags=["Health"])
async def root() -> dict:
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }
