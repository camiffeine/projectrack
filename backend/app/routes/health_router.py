'''System health and database monitoring routes (NFR-005, NFR-006)'''

from fastapi import APIRouter, status, Response
from config import settings
from database import Database

router = APIRouter(tags=["Health"])

@router.get("/health", summary="Application Liveness Check")
async def health_check():
    '''Returns basic liveness and version status for load balancers and deployment monitoring'''
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

@router.get("/health/db", summary="Database Connectivity & Latency Ping (NFR-005)")
async def database_health(response: Response):
    '''Pings the MongoDB database instance and returns round-trip latency metrics'''
    ping_result = Database.ping()

    if ping_result.get("status") != "healthy":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": ping_result
    }
