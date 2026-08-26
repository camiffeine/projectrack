'''Role service class with constructor dependency injection (NFR-009)'''

from typing import Optional, Dict, Any, List
from .base_service import BaseService
from factories.role_factory import RoleFactory
from repository.role_repo import RoleRepository
from models.role_model import RoleModel

# mvc (controller/service)

class RoleService(BaseService):
    '''Process business logic for roles'''

    def __init__(self, factory: Optional[RoleFactory] = None, repo: Optional[RoleRepository] = None):
        super().__init__(
            factory=factory or RoleFactory(),
            repo=repo or RoleRepository()
        )

    def add(self, role_data: RoleModel) -> Dict[str, Any]:
        '''Adds a role to the database'''
        return super().add(role_data, "Role")

    def get(self, role_id: int) -> Dict[str, Any]:
        '''Gets a role from the database'''
        return super().get(role_id, "Role")

    def update(self, role_id: int, updates: dict) -> Dict[str, Any]:
        '''Updates a role in the database'''
        return super().update(role_id, updates, "Role")

    def delete(self, role_id: int) -> Dict[str, Any]:
        '''Deletes a role from the database'''
        return super().delete(role_id, "Role")

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        '''Gets all roles from the database'''
        return super().get_all(skip=skip, limit=limit)
