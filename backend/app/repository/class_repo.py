'''Repository for the class (students group) entity'''

from .base_repo import BaseRepository
from database import get_db
from models.class_model import ClassModel

# repository

class ClassRepository(BaseRepository):
    '''Repository class for class modifications in database'''

    def __init__(self):
        '''Initializes class's repository'''
        self.collection = get_db()["classes"]  # References its respective collection

    def add(self, class_data: ClassModel):
        '''Adds a class to the database'''
        class_dict = class_data.model_dump(exclude={'class_id'})
        return super().add(class_dict)

    def get(self, class_id: int):
        '''Gets a class from the database'''
        return super().get(class_id)

    def update(self, class_id: int, updates: dict):
        '''Updates a class from the database'''
        return super().update(class_id, updates)

    def delete(self, class_id: int):
        '''Deletes a class from the database'''
        return super().delete(class_id)

    def get_by_professor(self, professor_id: int, skip: int = 0, limit: int = 100):
        '''Gets all classes taught by a professor with pagination (FR-004)'''
        cursor = self.find_many({"professor_id": professor_id}, skip=skip, limit=limit)
        return list(cursor)
