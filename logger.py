from loguru import logger
from pathlib import Path


log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logger.add(
    log_dir / "fast_command_{time:YYYY-MM-DD_HH}.log",
    rotation="1 hour",
    retention="7 days",
    compression="zip",
    enqueue=True,
    backtrace=True,
    diagnose=True
)

logger.info("Logger initialized.")
