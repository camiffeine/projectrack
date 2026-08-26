'''Class service class with constructor dependency injection (NFR-009)'''

from typing import Optional, Dict, Any, List
from .base_service import BaseService
from factories.class_factory import ClassFactory
from repository.class_repo import ClassRepository
from models.class_model import ClassModel

# mvc (controller/service)

class ClassService(BaseService):
    '''Process business logic for classes'''

    def __init__(self, factory: Optional[ClassFactory] = None, repo: Optional[ClassRepository] = None):
        super().__init__(
            factory=factory or ClassFactory(),
            repo=repo or ClassRepository()
        )

    def add(self, class_data: ClassModel) -> Dict[str, Any]:
        '''Adds a class to the database (FR-004)'''
        return super().add(class_data, "Class")

    def get(self, class_id: int) -> Dict[str, Any]:
        '''Gets a class from the database'''
        return super().get(class_id, "Class")

    def update(self, class_id: int, updates: dict) -> Dict[str, Any]:
        '''Updates a class in the database'''
        return super().update(class_id, updates, "Class")

    def delete(self, class_id: int) -> Dict[str, Any]:
        '''Deletes a class from the database'''
        return super().delete(class_id, "Class")

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        '''Gets all classes from the database'''
        return super().get_all(skip=skip, limit=limit)
