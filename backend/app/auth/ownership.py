'''Resource-level ownership verification guards (Area 10, NFR-004)'''

from typing import Dict, Any, Optional
from exceptions import ForbiddenException, EntityNotFoundException
from repository.student_repo import StudentRepository
from repository.professor_repo import ProfessorRepository
from repository.class_repo import ClassRepository
from repository.assignment_repo import AssignmentRepository
from repository.submission_repo import SubmissionRepository

def get_student_id_for_user(user_id: int, student_repo: Optional[StudentRepository] = None) -> int:
    '''Looks up student_id associated with user_id, raising ForbiddenException if not found'''
    repo = student_repo or StudentRepository()
    student = repo.get_by_user_id(user_id)
    if not student:
        raise ForbiddenException("User does not have an associated student profile.")
    return student["_id"]

def get_professor_id_for_user(user_id: int, prof_repo: Optional[ProfessorRepository] = None) -> int:
    '''Looks up professor_id associated with user_id, raising ForbiddenException if not found'''
    repo = prof_repo or ProfessorRepository()
    prof = repo.get_by_user_id(user_id)
    if not prof:
        raise ForbiddenException("User does not have an associated professor profile.")
    return prof["_id"]

def verify_user_access(target_user_id: int, current_user: Dict[str, Any]):
    '''Ensures current user can only access their own user record unless Admin or Professor'''
    if current_user.get("role") in (2, 3):
        return
    if current_user.get("user_id") != target_user_id:
        raise ForbiddenException("You do not have permission to access another user's record.")

def verify_user_update_access(target_user_id: int, current_user: Dict[str, Any]):
    '''Ensures current user can only modify their own user record unless Admin'''
    if current_user.get("role") == 3:
        return
    if current_user.get("user_id") != target_user_id:
        raise ForbiddenException("You do not have permission to modify another user's record.")

def verify_student_access(
    target_student_id: int,
    current_user: Dict[str, Any],
    student_repo: Optional[StudentRepository] = None
):
    '''Ensures student can only access their own resources (Professors and Admins bypass)'''
    role = current_user.get("role")
    if role in (2, 3):
        return

    user_id = current_user.get("user_id")
    caller_student_id = get_student_id_for_user(user_id, student_repo)
    if caller_student_id != target_student_id:
        raise ForbiddenException("You do not have permission to access another student's academic resources.")

def verify_class_ownership(
    class_id: int,
    current_user: Dict[str, Any],
    class_repo: Optional[ClassRepository] = None,
    prof_repo: Optional[ProfessorRepository] = None
):
    '''Ensures professor owns the class they are modifying (Admins bypass)'''
    role = current_user.get("role")
    if role == 3:
        return

    c_repo = class_repo or ClassRepository()
    class_doc = c_repo.get(class_id)
    if not class_doc:
        raise EntityNotFoundException("Class", class_id)

    user_id = current_user.get("user_id")
    prof_id = get_professor_id_for_user(user_id, prof_repo)
    if class_doc.get("professor_id") != prof_id:
        raise ForbiddenException("You do not have permission to modify or manage a class you do not teach.")

def verify_assignment_ownership(
    assignment_id: int,
    current_user: Dict[str, Any],
    assignment_repo: Optional[AssignmentRepository] = None,
    class_repo: Optional[ClassRepository] = None,
    prof_repo: Optional[ProfessorRepository] = None
):
    '''Ensures professor owns the class containing the assignment (Admins bypass)'''
    role = current_user.get("role")
    if role == 3:
        return

    a_repo = assignment_repo or AssignmentRepository()
    assignment = a_repo.get(assignment_id)
    if not assignment:
        raise EntityNotFoundException("Assignment", assignment_id)

    verify_class_ownership(assignment.get("class_id"), current_user, class_repo, prof_repo)

def verify_submission_access(
    submission_id: int,
    current_user: Dict[str, Any],
    submission_repo: Optional[SubmissionRepository] = None,
    student_repo: Optional[StudentRepository] = None
):
    '''Ensures student only views/updates their own submission (Professors and Admins bypass)'''
    role = current_user.get("role")
    if role in (2, 3):
        return

    s_repo = submission_repo or SubmissionRepository()
    sub = s_repo.get(submission_id)
    if not sub:
        raise EntityNotFoundException("Submission", submission_id)

    user_id = current_user.get("user_id")
    caller_student_id = get_student_id_for_user(user_id, student_repo)
    if sub.get("student_id") != caller_student_id:
        raise ForbiddenException("You do not have permission to access another student's submission.")
