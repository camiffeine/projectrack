"""Unit and integration tests for CORS Middleware and OpenAPI Documentation Polish (Area 9)"""

import pytest
from fastapi.testclient import TestClient
from main import app
from config import settings


@pytest.fixture
def client():
    """TestClient fixture for FastAPI app"""
    return TestClient(app)


def test_cors_allowed_origins_configuration():
    """Test that default allowed origins include standard frontend dev servers"""
    assert "http://localhost:3000" in settings.ALLOWED_ORIGINS
    assert "http://localhost:5173" in settings.ALLOWED_ORIGINS
    assert "http://127.0.0.1:3000" in settings.ALLOWED_ORIGINS
    assert "http://127.0.0.1:5173" in settings.ALLOWED_ORIGINS


def test_cors_preflight_request_allowed_origin(client):
    """Test CORS OPTIONS preflight request from allowed origin returns allow headers"""
    response = client.options(
        "/greeting/",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization,content-type",
        },
    )
    assert response.status_code == 200
    assert (
        response.headers.get("access-control-allow-origin") == "http://localhost:5173"
    )
    assert "GET" in response.headers.get("access-control-allow-methods", "")


def test_cors_preflight_request_disallowed_origin(client):
    """Test CORS OPTIONS preflight request from disallowed origin does not return allow origin header"""
    response = client.options(
        "/greeting/",
        headers={
            "Origin": "http://untrusted-site.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.headers.get("access-control-allow-origin") is None


def test_cors_get_request_allowed_origin(client):
    """Test simple GET request with Origin header gets back Access-Control-Allow-Origin"""
    response = client.get("/greeting/", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    assert (
        response.headers.get("access-control-allow-origin") == "http://localhost:3000"
    )


def test_openapi_schema_metadata(client):
    """Test that OpenAPI schema includes rich title, description, tags, contact, and license info"""
    response = client.get("/openapi.json")
    assert response.status_code == 200

    schema = response.json()
    info = schema.get("info", {})

    # Title, version, description
    assert info.get("title") == settings.APP_NAME
    assert info.get("version") == settings.APP_VERSION
    assert "ProjecTrack" in info.get("description", "")
    assert "RBAC" in info.get("description", "")

    # Contact & License
    assert info.get("contact", {}).get("name") == "ProjecTrack Dev Team"
    assert info.get("license", {}).get("name") == "GPL-3.0 License"

    # Tags metadata
    tag_names = [tag["name"] for tag in schema.get("tags", [])]
    expected_tags = [
        "Health",
        "Authentication",
        "Users",
        "Classes",
        "Assignments",
        "Submissions",
        "Roles",
    ]
    for expected in expected_tags:
        assert expected in tag_names
