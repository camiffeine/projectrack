'''Schemas module exporting all DTOs'''

from .common_schemas import MutationResponse
from .user_schemas import UserCreate, UserResponse, UserUpdate, RoleAssignment
from .auth_schemas import LoginRequest, TokenResponse
from .assignment_schemas import (
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentResponse,
    StudentAssignmentDetailResponse,
    MaterialAttachmentRequest
)
from .submission_schemas import (
    SubmissionCreate,
    SubmissionUpdate,
    SubmissionFeedbackRequest,
    SubmissionResponse
)
from .class_schemas import (
    ClassCreate,
    ClassUpdate,
    ClassEnrollmentRequest,
    ClassResponse,
    ClassStudentResponse
)
from .role_schemas import RoleCreate, RoleUpdate, RoleResponse
from .professor_schemas import ProfessorCreate, ProfessorUpdate, ProfessorResponse
from .student_schemas import StudentCreate, StudentUpdate, StudentResponse
from .student_assignment_schemas import (
    StudentAssignmentCreate,
    StudentAssignmentUpdate,
    StudentAssignmentResponse
)

__all__ = [
    'MutationResponse',
    'UserCreate',
    'UserResponse',
    'UserUpdate',
    'RoleAssignment',
    'LoginRequest',
    'TokenResponse',
    'AssignmentCreate',
    'AssignmentUpdate',
    'AssignmentResponse',
    'StudentAssignmentDetailResponse',
    'MaterialAttachmentRequest',
    'SubmissionCreate',
    'SubmissionUpdate',
    'SubmissionFeedbackRequest',
    'SubmissionResponse',
    'ClassCreate',
    'ClassUpdate',
    'ClassEnrollmentRequest',
    'ClassResponse',
    'ClassStudentResponse',
    'RoleCreate',
    'RoleUpdate',
    'RoleResponse',
    'ProfessorCreate',
    'ProfessorUpdate',
    'ProfessorResponse',
    'StudentCreate',
    'StudentUpdate',
    'StudentResponse',
    'StudentAssignmentCreate',
    'StudentAssignmentUpdate',
    'StudentAssignmentResponse'
]
