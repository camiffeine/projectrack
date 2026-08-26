'''Professor service class with constructor dependency injection (NFR-009)'''

from typing import Optional, Dict, Any, List
from .base_service import BaseService
from factories.professor_factory import ProfessorFactory
from models.professor_model import ProfessorModel
from repository.professor_repo import ProfessorRepository

# mvc (controller/service)

class ProfessorService(BaseService):
    '''Process business logic for professor entities'''

    def __init__(self, factory: Optional[ProfessorFactory] = None, repo: Optional[ProfessorRepository] = None):
        super().__init__(
            factory=factory or ProfessorFactory(),
            repo=repo or ProfessorRepository()
        )

    def add(self, professor_data: ProfessorModel) -> Dict[str, Any]:
        '''Adds a professor to the database'''
        return super().add(professor_data, "Professor")

    def get(self, professor_id: int) -> Dict[str, Any]:
        '''Gets a professor from the database'''
        return super().get(professor_id, "Professor")

    def update(self, professor_id: int, updates: dict) -> Dict[str, Any]:
        '''Updates a professor in the database'''
        return super().update(professor_id, updates, "Professor")

    def delete(self, professor_id: int) -> Dict[str, Any]:
        '''Deletes a professor from the database'''
        return super().delete(professor_id, "Professor")

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        '''Gets all professors from the database'''
        return super().get_all(skip=skip, limit=limit)
