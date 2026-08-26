'''Submission service class for student deliverables and professor grading (FR-010, FR-011, FR-012, NFR-009)'''

from typing import Optional, Dict, Any, List
from datetime import datetime
from .base_service import BaseService
from factories.submission_factory import SubmissionFactory
from repository.submission_repo import SubmissionRepository
from repository.assignment_repo import AssignmentRepository
from repository.student_repo import StudentRepository
from models.submission_model import SubmissionModel
from schemas.submission_schemas import SubmissionCreate
from exceptions import EntityNotFoundException, EntityAlreadyExistsException, BadRequestException

# mvc (controller/service)

class SubmissionService(BaseService):
    '''Process business logic for project deliverable submissions and grading'''

    def __init__(
        self,
        factory: Optional[SubmissionFactory] = None,
        repo: Optional[SubmissionRepository] = None,
        assignment_repo: Optional[AssignmentRepository] = None,
        student_repo: Optional[StudentRepository] = None
    ):
        super().__init__(
            factory=factory or SubmissionFactory(),
            repo=repo or SubmissionRepository()
        )
        self.assignment_repo = assignment_repo or AssignmentRepository()
        self.student_repo = student_repo or StudentRepository()

    def submit_assignment(self, submission_data: SubmissionCreate) -> Dict[str, Any]:
        '''Records a project deliverable submission from a student (FR-010, FR-012)'''
        # Check duplicate submission ID
        if self.repo.exists(submission_data.submission_id):
            raise EntityAlreadyExistsException("Submission", submission_data.submission_id)

        # Verify assignment exists
        if not self.assignment_repo.exists(submission_data.assignment_id):
            raise EntityNotFoundException("Assignment", submission_data.assignment_id)

        submission_model = SubmissionModel(
            submission_id=submission_data.submission_id,
            assignment_id=submission_data.assignment_id,
            student_id=submission_data.student_id,
            submission_date=datetime.now(),
            comment=submission_data.comment,
            attachment_url=submission_data.attachment_url,
            delivery_type=submission_data.delivery_type,
            status="SUBMITTED"
        )

        try:
            self.repo.add(submission_model)
            return self.repo.get(submission_data.submission_id)
        except Exception as e:
            raise BadRequestException(f"Failed to submit deliverable: {str(e)}")

    def provide_feedback(
        self,
        submission_id: int,
        feedback: str,
        grade: Optional[float] = None
    ) -> Dict[str, Any]:
        '''Records professor review comments and grade on a submission (FR-011)'''
        sub = self.repo.get(submission_id)
        if not sub:
            raise EntityNotFoundException("Submission", submission_id)

        try:
            self.repo.update_feedback(
                submission_id=submission_id,
                feedback=feedback,
                grade=grade,
                feedback_date=datetime.now()
            )
            return self.repo.get(submission_id)
        except Exception as e:
            raise BadRequestException(f"Failed to record feedback: {str(e)}")

    def get_submissions_by_assignment(
        self,
        assignment_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        '''Gets all submissions for an assignment for professor evaluation (FR-011)'''
        return self.repo.get_by_assignment(assignment_id, skip=skip, limit=limit)

    def get_submissions_by_student(
        self,
        student_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        '''Gets all submissions made by a student (FR-008)'''
        return self.repo.get_by_student(student_id, skip=skip, limit=limit)

    def add(self, submission: SubmissionModel) -> Dict[str, Any]:
        '''Adds a submission to the database (FR-010)'''
        return super().add(submission, "Submission")

    def get(self, submission_id: int) -> Dict[str, Any]:
        '''Gets a submission from the database'''
        return super().get(submission_id, "Submission")

    def update(self, submission_id: int, updates: dict) -> Dict[str, Any]:
        '''Updates a submission in the database'''
        return super().update(submission_id, updates, "Submission")

    def delete(self, submission_id: int) -> Dict[str, Any]:
        '''Deletes a submission from the database'''
        return super().delete(submission_id, "Submission")

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        '''Gets all submissions from the database'''
        return super().get_all(skip=skip, limit=limit)
