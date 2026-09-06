'''Professor schemas for request/response DTOs and update validation'''

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class ProfessorCreate(BaseModel):
    '''Schema for creating a professor'''
    professor_id: int = Field(..., gt=0, description="Professor ID")
    user_id: int = Field(..., gt=0, description="Associated User ID")

class ProfessorUpdate(BaseModel):
    '''Schema for updating professor details'''
    user_id: Optional[int] = Field(None, gt=0, description="Associated User ID")

class ProfessorResponse(BaseModel):
    '''Schema for returning professor details'''
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    professor_id: int = Field(alias="_id")
    user_id: int
