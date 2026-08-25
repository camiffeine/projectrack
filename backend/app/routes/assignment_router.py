'''Assignment router for handling endpoints'''

from fastapi import APIRouter, HTTPException, Depends

from .base_router import BaseRouter
from auth.auth_bearer import verify_auth, RoleRequired
from models.assignment_model import AssignmentModel
from services.assignment_service import AssignmentService

# mvc (view/api)

router = APIRouter()
base_router = BaseRouter()
base_router.service = AssignmentService()  # Dependency injection

# Assignment CRUD endpoints

@router.post("/assignments/add/", tags=["Assignments"], status_code=201, dependencies=[Depends(RoleRequired(2, 3))])
async def add_assignment(assignment: AssignmentModel):
    '''Add an assignment to the database (Professors & Admins - FR-005)'''
    return await base_router.add(assignment)

@router.get("/assignments/get/{assignment_id}", tags=["Assignments"], dependencies=[Depends(verify_auth)])
async def get_assignment(assignment_id: int):
    '''Get an assignment from the database (FR-008)'''
    return await base_router.get(assignment_id)

@router.put("/assignments/update/{assignment_id}", tags=["Assignments"], dependencies=[Depends(RoleRequired(2, 3))])
async def update_assignment(assignment_id: int, updates: dict):
    '''Update an assignment in the database (Professors & Admins)'''
    return await base_router.update(assignment_id, updates)

@router.delete("/assignments/delete/{assignment_id}", tags=["Assignments"], dependencies=[Depends(RoleRequired(2, 3))])
async def delete_assignment(assignment_id: int):
    '''Delete an assignment from the database (Professors & Admins)'''
    return await base_router.delete(assignment_id)

@router.get("/assignments/get/", tags=["Assignments"], dependencies=[Depends(verify_auth)])
async def get_assignments():
    '''Get all assignments from the database (FR-016)'''
    return await base_router.get_all()
