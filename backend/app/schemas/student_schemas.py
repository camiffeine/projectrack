'''Student schemas for request/response DTOs and update validation'''

from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class StudentCreate(BaseModel):
    '''Schema for creating a student'''
    student_id: int = Field(..., gt=0, description="Student ID")
    user_id: int = Field(..., gt=0, description="Associated User ID")
    class_id: List[int] = Field(default=[], description="List of enrolled class IDs")

class StudentUpdate(BaseModel):
    '''Schema for updating student details'''
    user_id: Optional[int] = Field(None, gt=0, description="Associated User ID")
    class_id: Optional[List[int]] = Field(None, description="List of enrolled class IDs")

class StudentResponse(BaseModel):
    '''Schema for returning student details'''
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    student_id: int = Field(alias="_id")
    user_id: int
    class_id: List[int] = Field(default=[])
