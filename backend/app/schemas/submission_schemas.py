'''Submission schemas for student deliveries and professor feedback (FR-010, FR-011, FR-012)'''

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class SubmissionCreate(BaseModel):
    '''Schema for student submitting a deliverable (FR-010, FR-012)'''
    submission_id: int = Field(..., gt=0, description="Submission ID")
    assignment_id: int = Field(..., gt=0, description="Assignment ID")
    student_id: int = Field(..., gt=0, description="Student ID")
    comment: Optional[str] = Field(None, max_length=500, description="Student submission comment")
    attachment_url: Optional[str] = Field(None, max_length=500, description="URL or link to project work")
    delivery_type: str = Field(default="FINAL", description="FINAL or PROGRESS")

class SubmissionFeedbackRequest(BaseModel):
    '''Schema for professor providing feedback and grade on a submission (FR-011)'''
    feedback: str = Field(..., min_length=1, max_length=1000, description="Professor review or feedback")
    grade: Optional[float] = Field(None, ge=0.0, le=100.0, description="Optional numerical score (0-100)")

class SubmissionResponse(BaseModel):
    '''Detailed submission response schema'''
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    submission_id: int = Field(alias="_id")
    assignment_id: int
    student_id: int
    submission_date: datetime
    comment: Optional[str] = None
    attachment_url: Optional[str] = None
    delivery_type: str
    status: str
    feedback: Optional[str] = None
    grade: Optional[float] = None
    feedback_date: Optional[datetime] = None
