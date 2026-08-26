'''Assignment service class with constructor dependency injection (NFR-009)'''

from typing import Optional, Dict, Any, List
from .base_service import BaseService
from factories.assignment_factory import AssignmentFactory
from models.assignment_model import AssignmentModel
from repository.assignment_repo import AssignmentRepository

# mvc (controller/service)

class AssignmentService(BaseService):
    '''Process business logic for assignments'''

    def __init__(self, factory: Optional[AssignmentFactory] = None, repo: Optional[AssignmentRepository] = None):
        super().__init__(
            factory=factory or AssignmentFactory(),
            repo=repo or AssignmentRepository()
        )

    def add(self, assignment: AssignmentModel) -> Dict[str, Any]:
        '''Adds an assignment to the database (FR-005)'''
        return super().add(assignment, "Assignment")

    def get(self, assignment_id: int) -> Dict[str, Any]:
        '''Gets an assignment from the database (FR-008)'''
        return super().get(assignment_id, "Assignment")

    def update(self, assignment_id: int, updates: dict) -> Dict[str, Any]:
        '''Updates an assignment in the database'''
        return super().update(assignment_id, updates, "Assignment")

    def delete(self, assignment_id: int) -> Dict[str, Any]:
        '''Deletes an assignment from the database'''
        return super().delete(assignment_id, "Assignment")

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        '''Gets all assignments from the database (FR-016)'''
        return super().get_all(skip=skip, limit=limit)
