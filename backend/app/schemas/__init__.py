'''Schemas module exporting all DTOs'''

from .user_schemas import UserCreate, UserResponse, UserUpdate, RoleAssignment
from .auth_schemas import LoginRequest, TokenResponse
from .assignment_schemas import (
    AssignmentCreate,
    AssignmentResponse,
    StudentAssignmentDetailResponse,
    MaterialAttachmentRequest
)
from .submission_schemas import SubmissionCreate, SubmissionFeedbackRequest, SubmissionResponse
from .class_schemas import (
    ClassCreate,
    ClassEnrollmentRequest,
    ClassResponse,
    ClassStudentResponse
)

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
    'MaterialAttachmentRequest',
    'SubmissionCreate',
    'SubmissionFeedbackRequest',
    'SubmissionResponse',
    'ClassCreate',
    'ClassEnrollmentRequest',
    'ClassResponse',
    'ClassStudentResponse'
]
