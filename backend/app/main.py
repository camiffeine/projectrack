'''Main module for the FastAPI application with lifespan management, DI, and centralized error handling (NFR-005, NFR-006, NFR-009)'''

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from config import settings
from database import Database
from repository.indexes import init_db_indexes
from exceptions import AppException
from routes import (
    health_router,
    auth,
    class_router,
    assignment_router,
    student_assignment_router,
    submission_router,
    role_router,
    professor_router,
    student_router,
    user_router
)

# Configure root logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("projectrack.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    '''FastAPI lifespan context manager: handles database startup, index creation, and shutdown'''
    # Startup phase
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}...")
    try:
        db = Database.connect()
        ping_res = Database.ping()
        logger.info(f"MongoDB Ping on boot: {ping_res}")
        init_db_indexes(db)
    except Exception as e:
        logger.warning(f"Database connection or indexing issue during startup: {e}")

    yield

    # Shutdown phase
    logger.info("Application shutting down. Closing database connection pool...")
    Database.disconnect()

# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="ProjecTrack Backend API for academic project tracking and assignment submissions.",
    lifespan=lifespan
)

# Centralized application exception handler
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    '''Formats all domain exceptions into standardized JSON responses'''
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Basic hello world test
@app.get("/greeting/", tags=["Greeting"])
async def hello_root():
    """Just a hello world message. :)"""
    return {"message": "Hello World!", "signs": "The ProjectTrack dev team"}

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint for the API"""
    return {"message": f"Welcome to the {settings.APP_NAME} API!", "version": settings.APP_VERSION}

# Include routers
app.include_router(health_router.router)
app.include_router(auth.router)

app.include_router(class_router.router)
app.include_router(assignment_router.router)
app.include_router(student_assignment_router.router)
app.include_router(submission_router.router)

app.include_router(role_router.router)
app.include_router(professor_router.router)
app.include_router(student_router.router)
app.include_router(user_router.router)
