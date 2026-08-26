'''Authentication routes with dependency injection (FR-001, FR-002)'''

from fastapi import APIRouter, HTTPException, status, Depends
from auth.auth_handler import create_access_token
from auth.security import verify_password
from services.user_service import UserService
from repository.user_repo import UserRepository
from schemas.auth_schemas import LoginRequest, TokenResponse
from schemas.user_schemas import UserCreate, UserResponse
from dependencies import get_user_service
from exceptions import UnauthorizedException

router = APIRouter(tags=["Auth"])

@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def register(user_data: UserCreate, service: UserService = Depends(get_user_service)):
    '''Public registration endpoint (FR-001): registers a new user with unassigned role (role_id=0)'''
    return service.register(user_data)

@router.post("/auth/login", response_model=TokenResponse)
@router.post("/login", response_model=TokenResponse, include_in_schema=False)
async def login(login_request: LoginRequest):
    '''User login endpoint (FR-002): authenticates credentials and returns JWT bearer token'''
    user_repo = UserRepository()
    user_db = user_repo.get_by_email(str(login_request.email))
    if not user_db or not verify_password(login_request.password, user_db['password']):
        raise UnauthorizedException("Invalid credentials")

    role_id = user_db.get('role_id', 0)
    user_id = user_db.get('_id')

    token_payload = {
        "sub": user_db['email'],
        "user_id": user_id,
        "role": role_id
    }
    token = create_access_token(token_payload)

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": role_id,
        "user_id": user_id
    }
