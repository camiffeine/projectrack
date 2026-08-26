'''Repository for the assignment entity (FR-005, FR-008, FR-016)'''

from typing import List, Dict, Any, Optional
from .base_repo import BaseRepository
from database import get_db
from models.assignment_model import AssignmentModel

# repository

class AssignmentRepository(BaseRepository):
    '''Repository class for assignment modifications and class/student assignment queries'''

    def __init__(self):
        '''Initializes assignment's repository'''
        self.collection = get_db()["assignments"]  # References its respective collection

    def add(self, assignment: AssignmentModel):
        '''Adds an assignment to the database'''
        assignment_dict = assignment.model_dump(exclude={'assignment_id'})
        return super().add(assignment_dict)

    def get(self, assignment_id: int):
        '''Gets an assignment from the database'''
        return super().get(assignment_id)

    def get_by_class_ids(self, class_ids: List[int]) -> List[Dict[str, Any]]:
        '''Gets all assignments belonging to the specified list of class IDs (FR-016)'''
        if not class_ids:
            return []
        return list(self.collection.find({"class_id": {"$in": class_ids}}))

    def get_by_ids(self, assignment_ids: List[int]) -> List[Dict[str, Any]]:
        '''Gets all assignments matching a given list of assignment IDs (FR-016)'''
        if not assignment_ids:
            return []
        return list(self.collection.find({"_id": {"$in": assignment_ids}}))

    def update(self, assignment_id: int, updates: dict):
        '''Updates an assignment in the database'''
        return super().update(assignment_id, updates)

    def delete(self, assignment_id: int):
        '''Deletes an assignment from the database'''
        return super().delete(assignment_id)

    def get_all(self, skip: int = 0, limit: int = 100):
        '''Gets all assignments from the database with pagination'''
        return super().get_all(skip=skip, limit=limit)
