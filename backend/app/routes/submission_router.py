'''Submission router with native FastAPI dependency injection (FR-010, FR-011, NFR-009)'''

from fastapi import APIRouter, Depends, status
from typing import List, Dict, Any

from auth.auth_bearer import verify_auth, RoleRequired
from models.submission_model import SubmissionModel
from services.submission_service import SubmissionService
from dependencies import get_submission_service, PaginationParams

router = APIRouter(tags=["Submissions"])

@router.post("/submissions/add/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(RoleRequired(1, 3))])
async def add_submission(
    submission: SubmissionModel,
    service: SubmissionService = Depends(get_submission_service)
):
    '''Add a project submission to the database (Students & Admins - FR-010)'''
    return service.add(submission)

@router.get("/submissions/get/{submission_id}", dependencies=[Depends(verify_auth)])
async def get_submission(
    submission_id: int,
    service: SubmissionService = Depends(get_submission_service)
):
    '''Get a submission from the database'''
    return service.get(submission_id)

@router.put("/submissions/update/{submission_id}", dependencies=[Depends(RoleRequired(1, 2, 3))])
async def update_submission(
    submission_id: int,
    updates: dict,
    service: SubmissionService = Depends(get_submission_service)
):
    '''Update a submission / provide feedback in the database (FR-011)'''
    return service.update(submission_id, updates)

@router.delete("/submissions/delete/{submission_id}", dependencies=[Depends(RoleRequired(3))])
async def delete_submission(
    submission_id: int,
    service: SubmissionService = Depends(get_submission_service)
):
    '''Delete a submission from the database (Admin only)'''
    return service.delete(submission_id)

@router.get("/submissions/get/", dependencies=[Depends(RoleRequired(2, 3))])
async def get_submissions(
    pagination: PaginationParams = Depends(),
    service: SubmissionService = Depends(get_submission_service)
):
    '''Get all submissions from the database with pagination (Professors & Admins - NFR-006)'''
    return service.get_all(skip=pagination.skip, limit=pagination.limit)
