'''Student Assignment schemas for request/response DTOs and update validation'''

from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class StudentAssignmentCreate(BaseModel):
    '''Schema for assigning students to an assignment'''
    assignment_id: int = Field(..., gt=0, description="Assignment ID")
    student_id: List[int] = Field(default=[], description="List of assigned student IDs")

class StudentAssignmentUpdate(BaseModel):
    '''Schema for updating assigned students list'''
    student_id: Optional[List[int]] = Field(None, description="List of assigned student IDs")

class StudentAssignmentResponse(BaseModel):
    '''Schema for returning student assignment details'''
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    assignment_id: int = Field(alias="_id")
    student_id: List[int] = Field(default=[])
