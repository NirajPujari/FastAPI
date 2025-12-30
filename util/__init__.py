from typing import Optional
import os
import logging
import sys

# ---------- Configuration & logging ----------
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def _get_env(
    key: str, required: bool = True, default: Optional[str] = None
) -> Optional[str]:
    val = os.getenv(key, default)
    if required and (val is None or val.strip() == ""):
        logger.error("Required environment variable %s is missing", key)
        sys.exit(1)
    return val
