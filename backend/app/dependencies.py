'''FastAPI dependency providers for services and pagination (NFR-009)'''

from fastapi import Query
from services.user_service import UserService
from services.assignment_service import AssignmentService
from services.class_service import ClassService
from services.role_service import RoleService
from services.submission_service import SubmissionService
from services.student_assignment_service import StudentAssignmentService
from services.professor_service import ProfessorService
from services.student_service import StudentService

class PaginationParams:
    '''Reusable pagination dependency extracting skip and limit query parameters'''
    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Number of items to skip for pagination"),
        limit: int = Query(20, ge=1, le=100, description="Maximum number of items to return (1-100)")
    ):
        self.skip = skip
        self.limit = limit

# Service Dependency Providers (can be overridden via app.dependency_overrides in tests)

def get_user_service() -> UserService:
    '''Returns an instance of UserService'''
    return UserService()

def get_assignment_service() -> AssignmentService:
    '''Returns an instance of AssignmentService'''
    return AssignmentService()

def get_class_service() -> ClassService:
    '''Returns an instance of ClassService'''
    return ClassService()

def get_role_service() -> RoleService:
    '''Returns an instance of RoleService'''
    return RoleService()

def get_submission_service() -> SubmissionService:
    '''Returns an instance of SubmissionService'''
    return SubmissionService()

def get_student_assignment_service() -> StudentAssignmentService:
    '''Returns an instance of StudentAssignmentService'''
    return StudentAssignmentService()

def get_professor_service() -> ProfessorService:
    '''Returns an instance of ProfessorService'''
    return ProfessorService()

def get_student_service() -> StudentService:
    '''Returns an instance of StudentService'''
    return StudentService()
