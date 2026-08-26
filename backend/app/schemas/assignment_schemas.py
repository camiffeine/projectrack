'''Assignment schemas for request/response DTOs (FR-005, FR-008, FR-016)'''

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class AssignmentCreate(BaseModel):
    '''Schema for professor creating an assignment (FR-005)'''
    assignment_id: int = Field(..., gt=0, description="Assignment ID")
    title: str = Field(..., min_length=3, max_length=80, description="Assignment title")
    description: str = Field(..., max_length=500, description="Assignment description")
    deadline: Optional[datetime] = Field(None, description="Deadline date and time")
    class_id: int = Field(..., gt=0, description="Class ID")
    status: str = Field(default="Active", description="Status: Active, Closed, Archived")

class AssignmentResponse(BaseModel):
    '''Schema for returning assignment details'''
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    assignment_id: int = Field(alias="_id")
    title: str
    description: str
    assignment_date: datetime
    deadline: Optional[datetime] = None
    class_id: int
    status: str

class StudentAssignmentDetailResponse(BaseModel):
    '''Enriched schema for student project tracking with submission status (FR-008, FR-016)'''
    assignment_id: int
    title: str
    description: str
    assignment_date: datetime
    deadline: Optional[datetime] = None
    class_id: int
    assignment_status: str
    submission_status: str = "PENDING"  # PENDING, SUBMITTED, FEEDBACK_PROVIDED
    submission_id: Optional[int] = None
    submission_date: Optional[datetime] = None
    attachment_url: Optional[str] = None
    grade: Optional[float] = None
    feedback: Optional[str] = None
