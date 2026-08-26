'''Repository for the submission entity (FR-010, FR-011, FR-012)'''

from typing import List, Dict, Any, Optional
from datetime import datetime
from .base_repo import BaseRepository
from database import get_db
from models.submission_model import SubmissionModel

# repository

class SubmissionRepository(BaseRepository):
    '''Repository class for project submissions and professor evaluations'''

    def __init__(self):
        '''Initializes submission's repository'''
        self.collection = get_db()["submissions"]  # References its respective collection

    def add(self, submission: SubmissionModel):
        '''Adds a submission to the database'''
        submission_dict = submission.model_dump(exclude={'submission_id'})
        return super().add(submission_dict)

    def get(self, submission_id: int) -> Optional[Dict[str, Any]]:
        '''Gets a submission from the database'''
        return super().get(submission_id)

    def get_by_student_and_assignment(self, student_id: int, assignment_id: int) -> Optional[Dict[str, Any]]:
        '''Finds a student's submission for a given assignment (FR-008, FR-010)'''
        return self.collection.find_one({"student_id": student_id, "assignment_id": assignment_id})

    def get_by_student(self, student_id: int, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        '''Finds all submissions made by a student (FR-008)'''
        return list(self.collection.find({"student_id": student_id}).skip(skip).limit(limit))

    def get_by_assignment(self, assignment_id: int, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        '''Finds all submissions for a given assignment for professor review (FR-011)'''
        return list(self.collection.find({"assignment_id": assignment_id}).skip(skip).limit(limit))

    def update_feedback(
        self,
        submission_id: int,
        feedback: str,
        grade: Optional[float] = None,
        feedback_date: Optional[datetime] = None
    ):
        '''Updates feedback, grade, and status on a submission (FR-011)'''
        update_data = {
            "feedback": feedback,
            "grade": grade,
            "status": "FEEDBACK_PROVIDED",
            "feedback_date": feedback_date or datetime.now()
        }
        return self.collection.update_one({"_id": submission_id}, {"$set": update_data})

    def update(self, submission_id: int, updates: dict):
        return super().update(submission_id, updates)

    def delete(self, submission_id: int):
        return super().delete(submission_id)

    def get_all(self, skip: int = 0, limit: int = 100):
        return super().get_all(skip=skip, limit=limit)
