'''Submission router with student deliveries and professor feedback grading (FR-010, FR-011, FR-012, NFR-009)'''

from fastapi import APIRouter, Depends, status
from typing import List, Dict, Any, Union

from auth.auth_bearer import verify_auth, RoleRequired, get_current_user
from auth.ownership import verify_student_access, verify_submission_access
from models.submission_model import SubmissionModel
from services.submission_service import SubmissionService
from schemas.submission_schemas import (
    SubmissionCreate,
    SubmissionUpdate,
    SubmissionFeedbackRequest,
    SubmissionResponse
)
from schemas.common_schemas import MutationResponse
from dependencies import get_submission_service, PaginationParams

router = APIRouter(tags=["Submissions"])

@router.post(
    "/submissions/add/",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RoleRequired(1, 3))],
    summary="Submit a project deliverable (Students & Admins - FR-010, FR-012)"
)
@router.post(
    "/submissions/",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RoleRequired(1, 3))],
    include_in_schema=False
)
async def submit_assignment(
    submission: SubmissionCreate,
    current_user: dict = Depends(get_current_user),
    service: SubmissionService = Depends(get_submission_service)
):
    '''Submit a final or progress deliverable for an assigned project (FR-010, FR-012)'''
    verify_student_access(submission.student_id, current_user)
    return service.submit_assignment(submission)

@router.put(
    "/submissions/{submission_id}/feedback",
    response_model=SubmissionResponse,
    dependencies=[Depends(RoleRequired(2, 3))],
    summary="Provide professor feedback and grading on a submission (Professors & Admins - FR-011)"
)
async def provide_feedback(
    submission_id: int,
    feedback_data: SubmissionFeedbackRequest,
    service: SubmissionService = Depends(get_submission_service)
):
    '''Professor review comments and grading evaluation for a student submission (FR-011)'''
    return service.provide_feedback(
        submission_id=submission_id,
        feedback=feedback_data.feedback,
        grade=feedback_data.grade
    )

@router.get(
    "/submissions/get/{submission_id}",
    response_model=SubmissionResponse,
    dependencies=[Depends(verify_auth)]
)
async def get_submission(
    submission_id: int,
    current_user: dict = Depends(get_current_user),
    service: SubmissionService = Depends(get_submission_service)
):
    '''Get a submission by ID from the database'''
    verify_submission_access(submission_id, current_user)
    return service.get(submission_id)

@router.get(
    "/submissions/student/{student_id}",
    response_model=List[SubmissionResponse],
    dependencies=[Depends(verify_auth)],
    summary="Get all submissions made by a student (FR-008)"
)
async def get_student_submissions(
    student_id: int,
    pagination: PaginationParams = Depends(),
    current_user: dict = Depends(get_current_user),
    service: SubmissionService = Depends(get_submission_service)
):
    '''Get all submissions made by a student with pagination'''
    verify_student_access(student_id, current_user)
    return service.get_submissions_by_student(
        student_id=student_id,
        skip=pagination.skip,
        limit=pagination.limit
    )

@router.put("/submissions/update/{submission_id}", response_model=MutationResponse, dependencies=[Depends(RoleRequired(1, 2, 3))])
async def update_submission(
    submission_id: int,
    updates: SubmissionUpdate,
    current_user: dict = Depends(get_current_user),
    service: SubmissionService = Depends(get_submission_service)
):
    '''Update a submission in the database'''
    verify_submission_access(submission_id, current_user)
    return service.update(submission_id, updates.model_dump(exclude_unset=True))

@router.delete("/submissions/delete/{submission_id}", response_model=MutationResponse, dependencies=[Depends(RoleRequired(3))])
async def delete_submission(
    submission_id: int,
    service: SubmissionService = Depends(get_submission_service)
):
    '''Delete a submission from the database (Admin only)'''
    return service.delete(submission_id)

@router.get("/submissions/get/", response_model=List[SubmissionResponse], dependencies=[Depends(RoleRequired(2, 3))])
async def get_submissions(
    pagination: PaginationParams = Depends(),
    service: SubmissionService = Depends(get_submission_service)
):
    '''Get all submissions from the database with pagination (Professors & Admins - NFR-006)'''
    return service.get_all(skip=pagination.skip, limit=pagination.limit)
