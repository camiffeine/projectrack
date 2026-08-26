'''User service class with constructor dependency injection and domain exceptions (NFR-009)'''

from typing import Optional, Dict, Any, List
from pydantic import SecretStr
from auth.security import hash_password
from .base_service import BaseService
from factories.user_factory import UserFactory
from models.user_model import UserModel
from repository.user_repo import UserRepository
from repository.role_repo import RoleRepository
from schemas.user_schemas import UserCreate
from exceptions import EntityNotFoundException, EntityAlreadyExistsException, BadRequestException

# mvc (controller/service)

class UserService(BaseService):
    '''Process business logic for user management, registration, and role assignment'''

    def __init__(
        self,
        factory: Optional[UserFactory] = None,
        repo: Optional[UserRepository] = None,
        role_repo: Optional[RoleRepository] = None
    ):
        factory_instance = factory or UserFactory()
        repo_instance = repo or UserRepository()
        super().__init__(factory=factory_instance, repo=repo_instance)
        self.role_repo = role_repo or RoleRepository()

    def register(self, user_data: UserCreate) -> Dict[str, Any]:
        '''Registers a new user with unassigned role (role_id=0) and hashed password (FR-001)'''
        if self.repo.exists(user_data.user_id):
            raise EntityAlreadyExistsException("User", user_data.user_id)

        existing_email = self.repo.get_by_email(user_data.email)
        if existing_email:
            raise BadRequestException(f"Email '{user_data.email}' is already registered.")

        plain_password = user_data.password.get_secret_value() if isinstance(user_data.password, SecretStr) else str(user_data.password)
        hashed = hash_password(plain_password)

        user_model = UserModel(
            user_id=user_data.user_id,
            first_name=user_data.first_name,
            middle_name=user_data.middle_name,
            last_name=user_data.last_name,
            second_last_name=user_data.second_last_name,
            email=user_data.email,
            password=SecretStr(hashed),
            sign_up_date=user_data.sign_up_date,
            role_id=0
        )

        try:
            self.repo.add(user_model)
            created_user = self.repo.get(user_data.user_id)
            return created_user
        except Exception as e:
            raise BadRequestException(f"Failed to register user: {str(e)}")

    def assign_role(self, user_id: int, role_id: int) -> Dict[str, Any]:
        '''Assigns a role to a user, validated by admin (FR-003)'''
        if not self.repo.exists(user_id):
            raise EntityNotFoundException("User", user_id)

        if role_id != 0:
            if not self.role_repo.exists(role_id):
                raise EntityNotFoundException("Role", role_id)

        try:
            self.repo.update_role(user_id, role_id)
            return {
                "msg": f"Role {role_id} assigned successfully to user {user_id}.",
                "user_id": user_id,
                "role_id": role_id
            }
        except Exception as e:
            raise BadRequestException(f"Failed to assign role: {str(e)}")

    def add(self, user: UserModel) -> Dict[str, Any]:
        '''Adds a user to the database (admin flow)'''
        existing_email = self.repo.get_by_email(user.email)
        if existing_email and existing_email.get("_id") != user.user_id:
            raise BadRequestException(f"Email '{user.email}' is already in use by another user.")

        raw_pwd = user.password.get_secret_value() if isinstance(user.password, SecretStr) else str(user.password)
        if not raw_pwd.startswith("$2b$") and not raw_pwd.startswith("$2a$"):
            user.password = SecretStr(hash_password(raw_pwd))

        return super().add(user, "User")

    def get(self, user_id: int) -> Dict[str, Any]:
        '''Gets a user from the database'''
        return super().get(user_id, "User")

    def update(self, user_id: int, updates: dict) -> Dict[str, Any]:
        '''Updates a user in the database with secure password hashing'''
        if 'password' in updates and updates['password']:
            pwd_val = updates['password'].get_secret_value() if isinstance(updates['password'], SecretStr) else str(updates['password'])
            if not pwd_val.startswith("$2b$") and not pwd_val.startswith("$2a$"):
                updates['password'] = hash_password(pwd_val)
        return super().update(user_id, updates, "User")

    def delete(self, user_id: int) -> Dict[str, Any]:
        '''Deletes a user from the database'''
        return super().delete(user_id, "User")

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        '''Gets all users from the database'''
        return super().get_all(skip=skip, limit=limit)
