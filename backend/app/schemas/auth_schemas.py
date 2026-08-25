'''Authentication schemas for login and token responses'''

from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    '''Schema for user login request (supports both user_email and email)'''
    email: EmailStr = Field(..., alias="user_email", description="User's email address")
    password: str = Field(..., alias="user_password", description="User's plain password")

    model_config = {
        "populate_by_name": True
    }

class TokenResponse(BaseModel):
    '''Schema for successful login response with JWT token'''
    access_token: str
    token_type: str = "bearer"
    role: int
    user_id: int
