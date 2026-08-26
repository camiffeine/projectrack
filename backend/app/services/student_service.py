'''Student service class with constructor dependency injection (NFR-009)'''

from typing import Optional, Dict, Any, List
from .base_service import BaseService
from factories.student_factory import StudentFactory
from models.student_model import StudentModel
from repository.student_repo import StudentRepository

# mvc (controller/service)

class StudentService(BaseService):
    '''Process business logic for student entities'''

    def __init__(self, factory: Optional[StudentFactory] = None, repo: Optional[StudentRepository] = None):
        super().__init__(
            factory=factory or StudentFactory(),
            repo=repo or StudentRepository()
        )

    def add(self, student_data: StudentModel) -> Dict[str, Any]:
        '''Adds a student to the database'''
        return super().add(student_data, "Student")

    def get(self, student_id: int) -> Dict[str, Any]:
        '''Gets a student from the database'''
        return super().get(student_id, "Student")

    def update(self, student_id: int, updates: dict) -> Dict[str, Any]:
        '''Updates a student in the database'''
        return super().update(student_id, updates, "Student")

    def delete(self, student_id: int) -> Dict[str, Any]:
        '''Deletes a student from the database'''
        return super().delete(student_id, "Student")

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        '''Gets all students from the database'''
        return super().get_all(skip=skip, limit=limit)
