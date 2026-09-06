'''Assignment service class with student assignment tracking and status aggregation (FR-005, FR-008, FR-016, NFR-009)'''

from typing import Optional, Dict, Any, List
from .base_service import BaseService
from factories.assignment_factory import AssignmentFactory
from models.assignment_model import AssignmentModel
from repository.assignment_repo import AssignmentRepository
from repository.student_repo import StudentRepository
from repository.student_assignment_repo import StudentAssignmentRepository
from repository.submission_repo import SubmissionRepository

from exceptions import EntityNotFoundException

# mvc (controller/service)

class AssignmentService(BaseService):
    '''Process business logic for assignments, materials, and student assignment discovery'''

    def __init__(
        self,
        factory: Optional[AssignmentFactory] = None,
        repo: Optional[AssignmentRepository] = None,
        student_repo: Optional[StudentRepository] = None,
        student_assign_repo: Optional[StudentAssignmentRepository] = None,
        submission_repo: Optional[SubmissionRepository] = None
    ):
        super().__init__(
            factory=factory or AssignmentFactory(),
            repo=repo or AssignmentRepository()
        )
        self.student_repo = student_repo or StudentRepository()
        self.student_assign_repo = student_assign_repo or StudentAssignmentRepository()
        self.submission_repo = submission_repo or SubmissionRepository()

    def add(self, assignment: AssignmentModel) -> Dict[str, Any]:
        '''Adds an assignment to the database (FR-005)'''
        return super().add(assignment, "Assignment")

    def get(self, assignment_id: int) -> Dict[str, Any]:
        '''Gets an assignment from the database (FR-008)'''
        return super().get(assignment_id, "Assignment")

    def get_student_assignments(self, student_id: int) -> List[Dict[str, Any]]:
        '''Finds all assignments for a student with live submission status and materials (FR-008, FR-013, FR-016)'''
        # 1. Look up student profile to find enrolled classes
        student = self.student_repo.get(student_id)
        enrolled_class_ids = student.get("class_id", []) if student else []

        # 2. Get assignments from enrolled classes
        class_assignments = self.repo.get_by_class_ids(enrolled_class_ids)

        # 3. Get assignments directly assigned to the student
        direct_assignment_ids = self.student_assign_repo.get_assignments_for_student(student_id)
        direct_assignments = self.repo.get_by_ids(direct_assignment_ids)

        # 4. Merge and deduplicate assignments
        all_assignments_map = {}
        for a in class_assignments + direct_assignments:
            all_assignments_map[a["_id"]] = a

        # 5. Decorate with student's submission status
        result = []
        for aid, a in all_assignments_map.items():
            sub = self.submission_repo.get_by_student_and_assignment(student_id, aid)

            sub_status = "PENDING"
            if sub:
                sub_status = sub.get("status", "SUBMITTED")

            item = {
                "assignment_id": a["_id"],
                "title": a.get("title", ""),
                "description": a.get("description", ""),
                "assignment_date": a.get("assignment_date"),
                "deadline": a.get("deadline"),
                "class_id": a.get("class_id", 0),
                "assignment_status": a.get("status", "Active"),
                "materials": a.get("materials", []),
                "submission_status": sub_status,
                "submission_id": sub.get("_id") if sub else None,
                "submission_date": sub.get("submission_date") if sub else None,
                "attachment_url": sub.get("attachment_url") if sub else None,
                "grade": sub.get("grade") if sub else None,
                "feedback": sub.get("feedback") if sub else None
            }
            result.append(item)

        return result

    def add_materials(self, assignment_id: int, materials: List[str]) -> Dict[str, Any]:
        '''Adds materials/guides to an assignment (FR-013)'''
        if not self.repo.exists(assignment_id):
            raise EntityNotFoundException("Assignment", assignment_id)

        self.repo.add_materials(assignment_id, materials)
        return {
            "message": f"Materials added to assignment {assignment_id} successfully.",
            "assignment_id": assignment_id,
            "materials": materials
        }

    def remove_material(self, assignment_id: int, material_url: str) -> Dict[str, Any]:
        '''Removes a material/guide from an assignment (FR-013)'''
        if not self.repo.exists(assignment_id):
            raise EntityNotFoundException("Assignment", assignment_id)

        self.repo.remove_material(assignment_id, material_url)
        return {
            "message": f"Material removed from assignment {assignment_id} successfully.",
            "assignment_id": assignment_id,
            "material_url": material_url
        }

    def update(self, assignment_id: int, updates: dict) -> Dict[str, Any]:
        '''Updates an assignment in the database'''
        return super().update(assignment_id, updates, "Assignment")

    def delete(self, assignment_id: int) -> Dict[str, Any]:
        '''Deletes an assignment from the database'''
        return super().delete(assignment_id, "Assignment")

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        '''Gets all assignments from the database (FR-016)'''
        return super().get_all(skip=skip, limit=limit)
