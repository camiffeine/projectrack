'''Role schemas for request/response DTOs and update validation'''

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class RoleCreate(BaseModel):
    '''Schema for creating a role'''
    role_id: int = Field(..., ge=0, description="Role ID (0=Unassigned, 1=Student, 2=Professor, 3=Admin)")
    role_name: str = Field(..., min_length=3, max_length=20, description="Role name")
    description: str = Field(..., min_length=3, max_length=50, description="Role description")

class RoleUpdate(BaseModel):
    '''Schema for updating role details'''
    role_name: Optional[str] = Field(None, min_length=3, max_length=20, description="Role name")
    description: Optional[str] = Field(None, min_length=3, max_length=50, description="Role description")

class RoleResponse(BaseModel):
    '''Schema for returning role details'''
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    role_id: int = Field(alias="_id")
    role_name: str
    description: str
