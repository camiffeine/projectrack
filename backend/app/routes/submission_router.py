'''Submission router for handling endpoints'''

from fastapi import APIRouter, HTTPException, Depends

from .base_router import BaseRouter
from auth.auth_bearer import verify_auth, RoleRequired
from models.submission_model import SubmissionModel
from services.submission_service import SubmissionService

# mvc (view/api)

router = APIRouter()
base_router = BaseRouter()
base_router.service = SubmissionService()  # Dependency injection

# Submission CRUD endpoints

@router.post("/submissions/add/", tags=["Submissions, Assignments"], status_code=201, dependencies=[Depends(RoleRequired(1, 3))])
async def add_submission(submission: SubmissionModel):
    '''Add a project submission to the database (Students & Admins - FR-010)'''
    return await base_router.add(submission)

@router.get("/submissions/get/{submission_id}", tags=["Submissions, Assignments"], dependencies=[Depends(verify_auth)])
async def get_submission(submission_id: int):
    '''Get a submission from the database'''
    return await base_router.get(submission_id)

@router.put("/submissions/update/{submission_id}", tags=["Submissions, Assignments"], dependencies=[Depends(RoleRequired(1, 2, 3))])
async def update_submission(submission_id: int, updates: dict):
    '''Update a submission / provide feedback in the database (FR-011)'''
    return await base_router.update(submission_id, updates)

@router.delete("/submissions/delete/{submission_id}", tags=["Submissions, Assignments"], dependencies=[Depends(RoleRequired(3))])
async def delete_submission(submission_id: int):
    '''Delete a submission from the database (Admin only)'''
    return await base_router.delete(submission_id)

@router.get("/submissions/get/", tags=["Submissions, Assignments"], dependencies=[Depends(RoleRequired(2, 3))])
async def get_submissions():
    '''Get all submissions from the database (Professors & Admins)'''
    return await base_router.get_all()
