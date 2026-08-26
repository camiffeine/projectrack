'''Student assignment service class with constructor dependency injection (NFR-009)'''

from typing import Optional, Dict, Any, List
from .base_service import BaseService
from factories.student_assignment_factory import StudentAssignmentFactory
from models.student_assignment_model import StudentAssignmentModel
from repository.student_assignment_repo import StudentAssignmentRepository

# mvc (controller/service)

class StudentAssignmentService(BaseService):
    '''Process business logic for student assignment mappings'''

    def __init__(self, factory: Optional[StudentAssignmentFactory] = None, repo: Optional[StudentAssignmentRepository] = None):
        super().__init__(
            factory=factory or StudentAssignmentFactory(),
            repo=repo or StudentAssignmentRepository()
        )

    def add(self, student_assignment: StudentAssignmentModel) -> Dict[str, Any]:
        '''Adds a student assignment mapping (FR-006)'''
        return super().add(student_assignment, "Student Assignment")

    def get(self, assignment_id: int) -> Dict[str, Any]:
        '''Gets a student assignment mapping'''
        return super().get(assignment_id, "Student Assignment")

    def update(self, assignment_id: int, updates: dict) -> Dict[str, Any]:
        '''Updates a student assignment mapping'''
        return super().update(assignment_id, updates, "Student Assignment")

    def delete(self, assignment_id: int) -> Dict[str, Any]:
        '''Deletes a student assignment mapping'''
        return super().delete(assignment_id, "Student Assignment")

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        '''Gets all student assignment mappings'''
        return super().get_all(skip=skip, limit=limit)
