import logging
from app.config import get_settings


def get_logger(name: str) -> logging.Logger:
    """Create and return a named logger with consistent formatting."""
    settings = get_settings()

    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    logger.propagate = False

    return logger
