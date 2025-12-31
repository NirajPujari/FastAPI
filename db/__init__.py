import sys
import time
import atexit
from typing import Optional
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.server_api import ServerApi
from type.db import CollectionName

from dotenv import load_dotenv
from util import _get_env, logger

# Load .env early
load_dotenv()

MONGO_DB_URL = _get_env("DB_URL")
MONGO_DB_NAME = _get_env("DB_NAME")

# ---------- Mongo client setup with retry ----------
_client: Optional[MongoClient] = None


def create_mongo_client(
    uri: str,
    server_api_version: str = "1",
    max_retries: int = 3,
    retry_delay: float = 1.0,
    server_selection_timeout_ms: int = 5000,
    connect_timeout_ms: int = 10000,
) -> MongoClient:
    """
    Create and return a connected MongoClient with basic retry/backoff.
    Exits the process if connection cannot be established.
    """
    global _client
    if _client:
        return _client

    attempt = 0
    last_exc: Optional[Exception] = None
    while attempt < max_retries:
        try:
            logger.info(
                "Attempting to connect to MongoDB (attempt %d/%d)...",
                attempt + 1,
                max_retries,
            )
            client = MongoClient(
                uri,
                server_api=ServerApi(server_api_version),
                serverSelectionTimeoutMS=server_selection_timeout_ms,
                connectTimeoutMS=connect_timeout_ms,
            )
            # Force a call to verify connection
            client.admin.command("ping")
            logger.info("Connected to MongoDB (database: %s)", MONGO_DB_NAME)
            _client = client
            return client
        except PyMongoError as exc:
            last_exc = exc
            logger.warning("MongoDB connection failed: %s", exc)
            attempt += 1
            if attempt < max_retries:
                sleep = retry_delay * (2 ** (attempt - 1))
                logger.info("Retrying in %.1f seconds...", sleep)
                time.sleep(sleep)

    logger.critical(
        "Could not connect to MongoDB after %d attempts. Exiting.", max_retries
    )
    if last_exc:
        logger.exception(last_exc)
    sys.exit(1)


# Create client (module import will try to connect)
client = create_mongo_client(MONGO_DB_URL)


# Ensure client is closed on process exit
def _close_client() -> None:
    global _client
    if _client:
        try:
            _client.close()
            logger.info("MongoDB client closed.")
        except Exception as exc:
            logger.debug("Error closing MongoDB client: %s", exc)


atexit.register(_close_client)

# ---------- Database & collections ----------
db = client[MONGO_DB_NAME]


# ---------- Optional utility accessors ----------
def get_db():
    return db


def get_collection(name: CollectionName):
    return db[name]
