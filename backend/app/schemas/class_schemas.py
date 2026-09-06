'''Class schemas for request/response DTOs and enrollment (FR-004)'''

from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class ClassCreate(BaseModel):
    '''Schema for creating a class (FR-004)'''
    class_id: int = Field(..., gt=0, description="Class ID")
    class_name: str = Field(..., min_length=3, max_length=50, description="Class name")
    professor_id: int = Field(..., gt=0, description="Professor ID who leads the class")

class ClassEnrollmentRequest(BaseModel):
    '''Schema for adding or removing a student from a class (FR-004)'''
    student_id: int = Field(..., gt=0, description="Student ID to enroll or unenroll")

class ClassUpdate(BaseModel):
    '''Schema for updating class details'''
    class_name: Optional[str] = Field(None, min_length=3, max_length=50, description="Class name")
    professor_id: Optional[int] = Field(None, gt=0, description="Professor ID who leads the class")

class ClassResponse(BaseModel):
    '''Schema for returning class details'''
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    class_id: int = Field(alias="_id")
    class_name: str
    professor_id: int

class ClassStudentResponse(BaseModel):
    '''Schema for returning student information within a class roster'''
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    student_id: int = Field(alias="_id")
    user_id: int
    class_id: List[int] = Field(default=[])
