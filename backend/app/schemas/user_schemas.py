'''User schemas for request and response Data Transfer Objects (DTOs)'''

from pydantic import BaseModel, Field, SecretStr, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    '''Schema for user registration (FR-001)'''
    user_id: int = Field(
        ..., gt=0, description="Must be a positive integer."
    )
    first_name: str = Field(
        ..., min_length=3, max_length=20, description="Name must be between 3 and 20 characters."
    )
    middle_name: Optional[str] = Field(
        None, min_length=3, max_length=20, description="Middle Name must be between 3 and 20 characters."
    )
    last_name: str = Field(
        ..., min_length=3, max_length=20, description="Last Name must be between 3 and 20 characters."
    )
    second_last_name: Optional[str] = Field(
        None, min_length=3, max_length=20, description="Second Last Name must be between 3 and 20 characters."
    )
    email: EmailStr = Field(
        ..., max_length=150, description="Email up to 150 characters."
    )
    password: SecretStr = Field(
        ..., min_length=8, max_length=200, description="Password must be between 8 and 200 characters."
    )
    sign_up_date: datetime = Field(
        default_factory=datetime.now, description="Date of sign up."
    )

class UserResponse(BaseModel):
    '''Schema for user responses without sensitive data like passwords'''
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    user_id: int = Field(alias="_id")
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    second_last_name: Optional[str] = None
    email: EmailStr
    sign_up_date: datetime
    role_id: int

class UserUpdate(BaseModel):
    '''Schema for updating user details'''
    first_name: Optional[str] = Field(None, min_length=3, max_length=20)
    middle_name: Optional[str] = Field(None, min_length=3, max_length=20)
    last_name: Optional[str] = Field(None, min_length=3, max_length=20)
    second_last_name: Optional[str] = Field(None, min_length=3, max_length=20)
    email: Optional[EmailStr] = Field(None, max_length=150)
    password: Optional[SecretStr] = Field(None, min_length=8, max_length=200)

class RoleAssignment(BaseModel):
    '''Schema for assigning a role to a user by Admin (FR-003)'''
    role_id: int = Field(
        ..., ge=0, description="Role ID to assign to the user."
    )
