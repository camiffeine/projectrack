'''Schemas module exporting all DTOs'''

from .user_schemas import UserCreate, UserResponse, UserUpdate, RoleAssignment
from .auth_schemas import LoginRequest, TokenResponse
from .assignment_schemas import AssignmentCreate, AssignmentResponse, StudentAssignmentDetailResponse
from .submission_schemas import SubmissionCreate, SubmissionFeedbackRequest, SubmissionResponse

__all__ = [
    'UserCreate',
    'UserResponse',
    'UserUpdate',
    'RoleAssignment',
    'LoginRequest',
    'TokenResponse',
    'AssignmentCreate',
    'AssignmentResponse',
    'StudentAssignmentDetailResponse',
    'SubmissionCreate',
    'SubmissionFeedbackRequest',
    'SubmissionResponse'
]
