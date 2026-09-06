'''Repository for the student entity'''

from .base_repo import BaseRepository
from database import get_db
from models.student_model import StudentModel

# repository

class StudentRepository(BaseRepository):
    '''Repository class for student modifications in database'''

    def __init__(self):
        '''Initializes student's repository'''
        self.collection = get_db()["students"]  # References its respective collection

    def add(self, student_data: StudentModel):
        '''Adds a student to the database'''
        student_dict = student_data.model_dump(exclude={'student_id'})
        return super().add(student_dict)

    def get(self, student_id: int):
        '''Gets a student from the database'''
        return super().get(student_id)

    def update(self, student_id: int, updates: dict):
        '''Updates a student in the database'''
        return super().update(student_id, updates)

    def delete(self, student_id: int):
        '''Deletes a student from the database'''
        return super().delete(student_id)

    def get_all(self, skip: int = 0, limit: int = 100):
        '''Gets all students from the database with pagination'''
        cursor = super().get_all(skip=skip, limit=limit)
        return list(cursor)

    def enroll_in_class(self, student_id: int, class_id: int):
        '''Enrolls a student in a class using $addToSet (FR-004)'''
        return self.collection.update_one(
            {"_id": student_id},
            {"$addToSet": {"class_id": class_id}}
        )

    def unenroll_from_class(self, student_id: int, class_id: int):
        '''Unenrolls a student from a class using $pull (FR-004)'''
        return self.collection.update_one(
            {"_id": student_id},
            {"$pull": {"class_id": class_id}}
        )

    def get_students_by_class(self, class_id: int, skip: int = 0, limit: int = 100):
        '''Gets all students enrolled in a class with pagination (FR-004)'''
        cursor = self.find_many({"class_id": class_id}, skip=skip, limit=limit)
        return list(cursor)
