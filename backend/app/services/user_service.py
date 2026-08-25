'''User service class that processes the business logic data for the user model'''

from auth.security import hash_password
from .base_service import BaseService
from factories.user_factory import UserFactory
from models.user_model import UserModel
from repository.user_repo import UserRepository
from repository.role_repo import RoleRepository
from schemas.user_schemas import UserCreate
from pydantic import SecretStr

# mvc (controller/service)

class UserService(BaseService):
    '''Process the business logic data for the user model'''

    def __init__(self):
        '''Initializes user's service'''
        self.factory = UserFactory()
        self.repo = UserRepository()
        self.role_repo = RoleRepository()

    def register(self, user_data: UserCreate):
        '''Registers a new user with unassigned role (role_id=0) and hashed password (FR-001)'''
        # Check if ID already exists
        existing_id = self.repo.get(user_data.user_id)
        if existing_id:
            return {"error": f"User ID {user_data.user_id} is already taken."}

        # Check if Email already exists
        existing_email = self.repo.get_by_email(user_data.email)
        if existing_email:
            return {"error": f"Email '{user_data.email}' is already registered."}

        # Convert password to hash
        plain_password = user_data.password.get_secret_value() if isinstance(user_data.password, SecretStr) else str(user_data.password)
        hashed = hash_password(plain_password)

        # Build domain model with unassigned role (0)
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
            return {"error": f"Failed to register user: {e}"}

    def assign_role(self, user_id: int, role_id: int):
        '''Assigns a role to a user, validated by admin (FR-003)'''
        user = self.repo.get(user_id)
        if not user:
            return {"error": f"User with ID {user_id} not found."}

        # Check role validity if role_id > 0
        if role_id != 0:
            role = self.role_repo.get(role_id)
            if not role:
                return {"error": f"Role ID {role_id} does not exist."}

        try:
            self.repo.update_role(user_id, role_id)
            return {"msg": f"Role {role_id} assigned successfully to user {user_id}.", "user_id": user_id, "role_id": role_id}
        except Exception as e:
            return {"error": f"Failed to assign role: {e}"}

    def add(self, user: UserModel):
        '''Adds a user to the database (admin flow)'''
        existing_email = self.repo.get_by_email(user.email)
        if existing_email and existing_email.get("_id") != user.user_id:
            return {"error": f"Email '{user.email}' is already in use by another user."}

        raw_pwd = user.password.get_secret_value() if isinstance(user.password, SecretStr) else str(user.password)
        # Only hash if it doesn't already appear to be a bcrypt hash ($2b$...)
        if not raw_pwd.startswith("$2b$") and not raw_pwd.startswith("$2a$"):
            user.password = SecretStr(hash_password(raw_pwd))

        return super().add(user, "User")

    def get(self, user_id: int):
        '''Gets a user from the database'''
        return super().get(user_id, "User")

    def update(self, user_id: int, updates: dict):
        '''Updates a user in the database with secure password hashing'''
        if 'password' in updates and updates['password']:
            pwd_val = updates['password'].get_secret_value() if isinstance(updates['password'], SecretStr) else str(updates['password'])
            if not pwd_val.startswith("$2b$") and not pwd_val.startswith("$2a$"):
                updates['password'] = hash_password(pwd_val)
        return super().update(user_id, updates, "User")

    def delete(self, user_id: int):
        '''Deletes a user from the database'''
        return super().delete(user_id, "User")

    def get_all(self):
        '''Gets all users from the database'''
        return super().get_all()
