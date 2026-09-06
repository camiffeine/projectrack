'''Repository for the professor entity'''

from .base_repo import BaseRepository
from database import get_db
from models.professor_model import ProfessorModel

# repository

class ProfessorRepository(BaseRepository):
    '''Repository class for professor modifications in database'''

    def __init__(self):
        '''Initializes professor's repository'''
        self.collection = get_db()["professors"]  # References its respective collection

    def add(self, professor_data: ProfessorModel):
        '''Adds a professor to the database'''
        professor_dict = professor_data.model_dump(exclude={'professor_id'})
        return super().add(professor_dict)

    def get(self, professor_id: int):
        '''Gets a professor from the database'''
        return super().get(professor_id)

    def update(self, professor_id: int, updates: dict):
        '''Updates a professor from the database'''
        return super().update(professor_id, updates)

    def delete(self, professor_id: int):
        '''Deletes a professor from the database'''
        return super().delete(professor_id)

    def get_by_user_id(self, user_id: int):
        '''Gets a professor profile by user ID'''
        return self.collection.find_one({"user_id": user_id})
