'''Authentication routes'''

from fastapi import APIRouter, HTTPException, status
from auth.auth_handler import create_access_token
from auth.security import verify_password
from services.user_service import UserService
from repository.user_repo import UserRepository
from schemas.auth_schemas import LoginRequest, TokenResponse
from schemas.user_schemas import UserCreate, UserResponse

router = APIRouter(tags=["Auth"])
user_service = UserService()
user_repo = UserRepository()

@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def register(user_data: UserCreate):
    '''Public registration endpoint (FR-001): registers a new user with unassigned role (role_id=0)'''
    result = user_service.register(user_data)
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
    return result

@router.post("/auth/login", response_model=TokenResponse)
@router.post("/login", response_model=TokenResponse, include_in_schema=False)
async def login(login_request: LoginRequest):
    '''User login endpoint (FR-002): authenticates credentials and returns JWT bearer token'''
    user_db = user_repo.get_by_email(str(login_request.email))
    if not user_db or not verify_password(login_request.password, user_db['password']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

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
