'''Repository for the Student Assignment entity (FR-006, FR-016)'''

from typing import List
from .base_repo import BaseRepository
from database import get_db
from models.student_assignment_model import StudentAssignmentModel

# repository

class StudentAssignmentRepository(BaseRepository):
    '''Repository class for Student Assignments modifications in database'''

    def __init__(self):
        '''Initializes students assignments' repository'''
        self.collection = get_db()["student_assignments"]  # References its respective collection

    def add(self, assignment: StudentAssignmentModel):
        '''Adds a student assignment to the database'''
        assignment_dict = assignment.model_dump(exclude={'assignment_id'})
        return super().add(assignment_dict)

    def get(self, assignment_id: int):
        '''Gets a student assignment from the database'''
        return super().get(assignment_id)

    def get_assignments_for_student(self, student_id: int) -> List[int]:
        '''Finds all assignment IDs explicitly assigned to this student ID (FR-016)'''
        cursor = self.collection.find({"student_id": student_id}, {"_id": 1})
        return [doc["_id"] for doc in cursor]

    def update(self, assignment_id: int, updates: dict):
        '''Updates a student assignment in the database'''
        return super().update(assignment_id, updates)

    def delete(self, assignment_id: int):
        '''Deletes a student assignment from the database'''
        return super().delete(assignment_id)

    def get_all(self, skip: int = 0, limit: int = 100):
        '''Gets all student assignments with pagination'''
        return super().get_all(skip=skip, limit=limit)
