'''Unit and integration tests for Authentication and RBAC functionality'''

import pytest
from pydantic import SecretStr
from fastapi import HTTPException

from auth.auth_handler import create_access_token, verify_token
from auth.auth_bearer import RoleRequired
from auth.security import hash_password, verify_password
from schemas.auth_schemas import LoginRequest, TokenResponse
from schemas.user_schemas import UserCreate, UserResponse, RoleAssignment

def test_password_hashing_and_verification():
    '''Test password hashing generates valid bcrypt hash and verifies correctly'''
    plain = "SuperSecret123!"
    hashed = hash_password(plain)

    assert hashed != plain
    assert hashed.startswith("$2b$") or hashed.startswith("$2a$")
    assert verify_password(plain, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_jwt_token_generation_and_verification():
    '''Test JWT creation and payload extraction with user_id and role'''
    payload = {
        "sub": "student@university.edu",
        "user_id": 101,
        "role": 1
    }
    token = create_access_token(payload)
    assert isinstance(token, str)

    decoded = verify_token(token)
    assert decoded is not None
    assert decoded["sub"] == "student@university.edu"
    assert decoded["user_id"] == 101
    assert decoded["role"] == 1
    assert "exp" in decoded
    assert "iat" in decoded

def test_jwt_verification_invalid_token():
    '''Test JWT verification returns None for invalid token'''
    assert verify_token("invalid.jwt.token") is None

@pytest.mark.asyncio
async def test_role_required_permits_allowed_role():
    '''Test RoleRequired allows matching role IDs'''
    guard = RoleRequired(2, 3) # Professor or Admin
    token_payload = {"sub": "prof@univ.edu", "user_id": 5, "role": 2}

    result = await guard(token_payload)
    assert result == token_payload

@pytest.mark.asyncio
async def test_role_required_rejects_disallowed_role():
    '''Test RoleRequired raises 403 for disallowed role IDs'''
    guard = RoleRequired(3) # Admin only
    token_payload = {"sub": "student@univ.edu", "user_id": 10, "role": 1}

    with pytest.raises(HTTPException) as exc_info:
        await guard(token_payload)

    assert exc_info.value.status_code == 403
    assert "Insufficient permissions" in exc_info.value.detail

def test_login_request_schema_compatibility():
    '''Test LoginRequest supports both user_email and email aliases'''
    req1 = LoginRequest(user_email="test@example.com", user_password="password123")
    assert req1.email == "test@example.com"
    assert req1.password == "password123"

    req2 = LoginRequest(email="test2@example.com", password="password456")
    assert req2.email == "test2@example.com"
    assert req2.password == "password456"

def test_user_response_schema_omits_password():
    '''Test UserResponse excludes password and properly maps _id to user_id'''
    db_doc = {
        "_id": 42,
        "first_name": "Ada",
        "middle_name": None,
        "last_name": "Lovelace",
        "second_last_name": None,
        "email": "ada@example.com",
        "password": "$2b$12$hashedpasswordthatshouldnotleak",
        "sign_up_date": "2026-08-15T00:00:00",
        "role_id": 1
    }

    user_resp = UserResponse.model_validate(db_doc)
    dump = user_resp.model_dump()

    assert dump["user_id"] == 42
    assert dump["email"] == "ada@example.com"
    assert dump["role_id"] == 1
    assert "password" not in dump

def test_user_create_schema_defaults_and_validation():
    '''Test UserCreate schema validation'''
    user_create = UserCreate(
        user_id=99,
        first_name="Alan",
        last_name="Turing",
        email="alan@example.com",
        password=SecretStr("EnigmaCracker123!")
    )

    assert user_create.user_id == 99
    assert user_create.first_name == "Alan"
    assert user_create.password.get_secret_value() == "EnigmaCracker123!"
