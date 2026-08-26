'''Submission service class with constructor dependency injection (NFR-009)'''

from typing import Optional, Dict, Any, List
from .base_service import BaseService
from factories.submission_factory import SubmissionFactory
from repository.submission_repo import SubmissionRepository
from models.submission_model import SubmissionModel

# mvc (controller/service)

class SubmissionService(BaseService):
    '''Process business logic for project submissions'''

    def __init__(self, factory: Optional[SubmissionFactory] = None, repo: Optional[SubmissionRepository] = None):
        super().__init__(
            factory=factory or SubmissionFactory(),
            repo=repo or SubmissionRepository()
        )

    def add(self, submission: SubmissionModel) -> Dict[str, Any]:
        '''Adds a submission to the database (FR-010)'''
        return super().add(submission, "Submission")

    def get(self, submission_id: int) -> Dict[str, Any]:
        '''Gets a submission from the database'''
        return super().get(submission_id, "Submission")

    def update(self, submission_id: int, updates: dict) -> Dict[str, Any]:
        '''Updates a submission in the database (FR-011)'''
        return super().update(submission_id, updates, "Submission")

    def delete(self, submission_id: int) -> Dict[str, Any]:
        '''Deletes a submission from the database'''
        return super().delete(submission_id, "Submission")

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        '''Gets all submissions from the database'''
        return super().get_all(skip=skip, limit=limit)
