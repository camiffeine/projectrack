'''Base service class with constructor dependency injection and domain exceptions (NFR-009)'''

from abc import ABC
from typing import Optional, Dict, Any, List
from factories.base_factory import BaseFactory
from models.base_entity_model import BaseEntityModel
from repository.base_repo import BaseRepository
from exceptions import EntityNotFoundException, EntityAlreadyExistsException, BadRequestException

# mvc (controller/service)

class BaseService(ABC):
    '''Base service class providing common CRUD operations with exception-based error handling'''

    def __init__(self, factory: Optional[BaseFactory] = None, repo: Optional[BaseRepository] = None):
        self.factory = factory
        self.repo = repo

    def add(self, entity_data: BaseEntityModel, entity_name: str) -> Dict[str, Any]:
        '''Adds a new entity, raising EntityAlreadyExistsException if ID already exists'''
        if self.repo.exists(entity_data.entity_id):
            raise EntityAlreadyExistsException(entity_name, entity_data.entity_id)

        try:
            new_entity = self.factory.create(entity_data) if self.factory else entity_data
            result = self.repo.add(new_entity)
            return {"msg": f"{entity_name} added successfully.", "id": str(result.inserted_id), "entity_id": entity_data.entity_id}
        except Exception as e:
            raise BadRequestException(f"Failed to add {entity_name}: {str(e)}")

    def get(self, entity_id: int, entity_name: str) -> Dict[str, Any]:
        '''Gets an entity by ID, raising EntityNotFoundException if missing'''
        item = self.repo.get(entity_id)
        if not item:
            raise EntityNotFoundException(entity_name, entity_id)
        return item

    def update(self, entity_id: int, updates: dict, entity_name: str) -> Dict[str, Any]:
        '''Updates an entity, raising EntityNotFoundException if missing'''
        if not self.repo.exists(entity_id):
            raise EntityNotFoundException(entity_name, entity_id)

        try:
            self.repo.update(entity_id, updates)
            return {"msg": f"{entity_name} updated successfully.", "entity_id": entity_id}
        except Exception as e:
            raise BadRequestException(f"Failed to update {entity_name}: {str(e)}")

    def delete(self, entity_id: int, entity_name: str) -> Dict[str, Any]:
        '''Deletes an entity, raising EntityNotFoundException if missing'''
        if not self.repo.exists(entity_id):
            raise EntityNotFoundException(entity_name, entity_id)

        try:
            self.repo.delete(entity_id)
            return {"msg": f"{entity_name} deleted successfully.", "entity_id": entity_id}
        except Exception as e:
            raise BadRequestException(f"Failed to delete {entity_name}: {str(e)}")

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        '''Gets entities with pagination'''
        try:
            retrieved_cursor = self.repo.get_all(skip=skip, limit=limit)
            return list(retrieved_cursor)
        except Exception as e:
            raise BadRequestException(f"Failed to retrieve entities: {str(e)}")
