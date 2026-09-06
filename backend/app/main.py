"""Main module for the FastAPI application with CORS, lifespan management, DI, and centralized error handling (NFR-001, NFR-005, NFR-006, NFR-009)"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

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
    user_router,
)

# Configure root logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("projectrack.main")

API_DESCRIPTION = """
## ProjecTrack Academic Project Tracking Platform

**ProjecTrack** is a modular, high-performance RESTful API designed for academic institutions to manage courses, project deliverables, and iterative professor-student feedback loops.

### Architecture Highlights
- **FastAPI Core**: Asynchronous ASGI framework with native Dependency Injection and Pydantic v2 data validation.
- **Role-Based Access Control (RBAC)**: Fine-grained security using JWT Bearer authentication:
  - `0 = Unassigned`: Registered users pending administrator role approval.
  - `1 = Student`: View enrolled courses, project assignments, upload deliverables, and track review feedback.
  - `2 = Professor`: Create groups/classes, issue project assignments, upload guides/rubrics, and grade deliverables.
  - `3 = Admin`: Full administrative control over system users, roles, and course records.
- **MongoDB Connection Pooling**: Configured with automated index initialization, connection pooling, and health latency observability.
"""

TAGS_METADATA = [
    {
        "name": "Health",
        "description": "Liveness probes and MongoDB connection latency health checks (NFR-005).",
    },
    {
        "name": "Authentication",
        "description": "User registration (`POST /auth/register`) and JWT authentication (`POST /auth/login`) (FR-001, FR-002).",
    },
    {
        "name": "Users",
        "description": "User profile management and Administrator role assignment (FR-003).",
    },
    {
        "name": "Classes",
        "description": "Course group management, student enrollment rosters, and professor schedules (FR-004).",
    },
    {
        "name": "Assignments",
        "description": "Academic project assignments, reference material guides, and student status tracking (FR-005, FR-008, FR-013, FR-016).",
    },
    {
        "name": "Submissions",
        "description": "Student project deliverables submission and professor review feedback/grading (FR-010, FR-011, FR-012).",
    },
    {
        "name": "Student Assignments",
        "description": "Direct student-to-assignment associations and team allocations.",
    },
    {
        "name": "Roles",
        "description": "System role definitions and access permissions.",
    },
    {
        "name": "Professors",
        "description": "Academic faculty profiles and departmental associations.",
    },
    {
        "name": "Students",
        "description": "Student academic profiles and enrollment histories.",
    },
    {
        "name": "Root",
        "description": "API entrypoint and platform versioning.",
    },
    {
        "name": "Greeting",
        "description": "Developer greeting and connectivity sanity check.",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager: handles database startup, index creation, and shutdown"""
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


# Initialize FastAPI application with OpenAPI metadata
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=API_DESCRIPTION,
    openapi_tags=TAGS_METADATA,
    contact={
        "name": "ProjecTrack Dev Team",
    },
    license_info={
        "name": "GPL-3.0 License",
        "url": "https://opensource.org/licenses/GPL-3.0",
    },
    lifespan=lifespan,
)

# CORS Middleware Configuration (NFR-001)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Centralized application exception handler
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Formats all domain exceptions into standardized JSON responses"""
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


# Basic hello world test
@app.get("/greeting/", tags=["Greeting"])
async def hello_root():
    """Just a hello world message. :)"""
    return {"message": "Hello World!", "signs": "The ProjectTrack dev team"}


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint for the API"""
    return {
        "message": f"Welcome to the {settings.APP_NAME} API!",
        "version": settings.APP_VERSION,
    }


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
