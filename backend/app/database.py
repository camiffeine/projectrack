'''Database connection and connection pool management (NFR-005, NFR-006)'''

import time
import logging
from pymongo import MongoClient
from pymongo.database import Database as MongoDatabase
from config import settings

logger = logging.getLogger("projectrack.database")

class Database:
    '''Database manager with connection pooling and lifecycle hooks'''
    _instance = None
    client: MongoClient = None
    db: MongoDatabase = None

    def __new__(cls):
        '''Creates or returns singleton instance'''
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._init_connection()
        return cls._instance

    def _init_connection(self):
        '''Initializes MongoClient with configured connection pool parameters'''
        if self.client is None:
            try:
                self.client = MongoClient(
                    settings.MONGO_URI,
                    minPoolSize=settings.MIN_POOL_SIZE,
                    maxPoolSize=settings.MAX_POOL_SIZE,
                    maxIdleTimeMS=settings.MAX_IDLE_TIME_MS,
                    connectTimeoutMS=settings.CONNECT_TIMEOUT_MS,
                    serverSelectionTimeoutMS=settings.SERVER_SELECTION_TIMEOUT_MS,
                )
                self.db = self.client[settings.MONGO_DB_NAME]
                logger.info(f"Connected to MongoDB database '{settings.MONGO_DB_NAME}' with pool [{settings.MIN_POOL_SIZE}-{settings.MAX_POOL_SIZE}]")
            except Exception as e:
                logger.error(f"Failed to initialize MongoDB client: {e}")
                self.client = None
                self.db = None

    @classmethod
    def connect(cls) -> MongoDatabase:
        '''Explicitly connects or returns existing connection during startup'''
        instance = cls()
        if instance.client is None:
            instance._init_connection()
        return instance.db

    @classmethod
    def disconnect(cls):
        '''Closes all socket connections in the pool during application shutdown'''
        if cls._instance and cls._instance.client is not None:
            try:
                cls._instance.client.close()
                logger.info("Closed MongoDB connection pool cleanly.")
            except Exception as e:
                logger.warning(f"Error while closing MongoDB client: {e}")
            finally:
                cls._instance.client = None
                cls._instance.db = None
                cls._instance = None

    @classmethod
    def ping(cls) -> dict:
        '''Measures database round-trip latency and verifies connectivity (NFR-005)'''
        instance = cls()
        if instance.client is None:
            return {"status": "disconnected", "latency_ms": None, "error": "Database client is not initialized"}
        try:
            start_time = time.perf_counter()
            instance.client.admin.command("ping")
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            return {
                "status": "healthy",
                "database": settings.MONGO_DB_NAME,
                "latency_ms": latency_ms
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "database": settings.MONGO_DB_NAME,
                "latency_ms": None,
                "error": str(e)
            }

    def __del__(self):
        '''Safe cleanup on garbage collection'''
        if getattr(self, 'client', None) is not None:
            try:
                self.client.close()
            except Exception:
                pass


def get_db() -> MongoDatabase:
    '''Dependency/Helper to obtain the active MongoDatabase instance'''
    return Database().db

def get_client() -> MongoClient:
    '''Helper to obtain the underlying MongoClient'''
    return Database().client
