'''Assignment model module with Pydantic validations (FR-005)'''

from typing import Optional, List
from datetime import datetime
from pydantic import Field, model_validator
from .base_entity_model import BaseEntityModel

# mvc (model)

class AssignmentModel(BaseEntityModel):
    '''Assignment domain model with validations (FR-005, FR-013)'''
    assignment_id: int = Field(
        ..., gt=0, description="Must be a positive integer."
    )

    title: str = Field(
        ..., min_length=3, max_length=80, description="Assignment title between 3 and 80 characters."
    )

    description: str = Field(
        ..., max_length=500, description="Assignment description up to 500 characters."
    )

    assignment_date: datetime = Field(
        default_factory=datetime.now, description="Date when the assignment was issued."
    )

    deadline: Optional[datetime] = Field(
        None, description="Assignment deadline timestamp."
    )

    class_id: int = Field(
        ..., gt=0, description="Class ID this assignment belongs to."
    )

    status: str = Field(
        default="Active", description="Status: Active, Closed, Archived"
    )

    materials: List[str] = Field(
        default=[], description="List of URLs or reference material links uploaded by the professor."
    )

    # Pydantic model validator
    @model_validator(mode='before')
    def set_entity_id(cls, values):
        values['entity_id'] = values.get('assignment_id')
        return values
