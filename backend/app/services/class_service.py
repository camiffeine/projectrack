'''Class service class with constructor dependency injection (FR-004, NFR-009)'''

from typing import Optional, Dict, Any, List
from .base_service import BaseService
from factories.class_factory import ClassFactory
from repository.class_repo import ClassRepository
from repository.student_repo import StudentRepository
from models.class_model import ClassModel
from exceptions import EntityNotFoundException

# mvc (controller/service)

class ClassService(BaseService):
    '''Process business logic for classes and student enrollment'''

    def __init__(
        self,
        factory: Optional[ClassFactory] = None,
        repo: Optional[ClassRepository] = None,
        student_repo: Optional[StudentRepository] = None
    ):
        super().__init__(
            factory=factory or ClassFactory(),
            repo=repo or ClassRepository()
        )
        self.student_repo = student_repo or StudentRepository()

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

    def enroll_student(self, class_id: int, student_id: int) -> Dict[str, Any]:
        '''Enrolls a student into a class (FR-004)'''
        if not self.repo.exists(class_id):
            raise EntityNotFoundException("Class", class_id)
        if not self.student_repo.exists(student_id):
            raise EntityNotFoundException("Student", student_id)

        self.student_repo.enroll_in_class(student_id, class_id)
        return {
            "message": f"Student {student_id} enrolled in class {class_id} successfully.",
            "class_id": class_id,
            "student_id": student_id
        }

    def unenroll_student(self, class_id: int, student_id: int) -> Dict[str, Any]:
        '''Unenrolls a student from a class (FR-004)'''
        if not self.repo.exists(class_id):
            raise EntityNotFoundException("Class", class_id)
        if not self.student_repo.exists(student_id):
            raise EntityNotFoundException("Student", student_id)

        self.student_repo.unenroll_from_class(student_id, class_id)
        return {
            "message": f"Student {student_id} unenrolled from class {class_id} successfully.",
            "class_id": class_id,
            "student_id": student_id
        }

    def get_enrolled_students(self, class_id: int, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        '''Gets all students enrolled in a specific class (FR-004)'''
        if not self.repo.exists(class_id):
            raise EntityNotFoundException("Class", class_id)
        return self.student_repo.get_students_by_class(class_id, skip=skip, limit=limit)

    def get_classes_by_professor(self, professor_id: int, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        '''Gets all classes taught by a professor (FR-004)'''
        return self.repo.get_by_professor(professor_id, skip=skip, limit=limit)
