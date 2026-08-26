'''Submission model module with Pydantic validations (FR-010, FR-011, FR-012)'''

from typing import Optional
from datetime import datetime
from pydantic import Field, model_validator
from .base_entity_model import BaseEntityModel

# mvc (model)

class SubmissionModel(BaseEntityModel):
    '''Submission domain model with deliverable and feedback attributes'''
    submission_id: int = Field(
        ..., gt=0, description="Must be a positive integer."
    )

    assignment_id: int = Field(
        ..., gt=0, description="Assignment ID being delivered."
    )

    student_id: int = Field(
        ..., gt=0, description="Student ID making the delivery."
    )

    submission_date: datetime = Field(
        default_factory=datetime.now, description="Timestamp when the deliverable was submitted."
    )

    comment: Optional[str] = Field(
        None, max_length=500, description="Student comment or submission notes."
    )

    attachment_url: Optional[str] = Field(
        None, max_length=500, description="URL or file link of the project delivery (FR-012)."
    )

    delivery_type: str = Field(
        default="FINAL", description="Delivery type: FINAL or PROGRESS (FR-009, FR-010)."
    )

    status: str = Field(
        default="SUBMITTED", description="Status: SUBMITTED, FEEDBACK_PROVIDED, GRADED."
    )

    feedback: Optional[str] = Field(
        None, max_length=1000, description="Professor review or feedback comment (FR-011)."
    )

    grade: Optional[float] = Field(
        None, ge=0.0, le=100.0, description="Evaluation grade/score assigned by professor."
    )

    feedback_date: Optional[datetime] = Field(
        None, description="Timestamp when professor provided feedback."
    )

    # Pydantic model validator
    @model_validator(mode='before')
    def set_entity_id(cls, values):
        values['entity_id'] = values.get('submission_id')
        return values
