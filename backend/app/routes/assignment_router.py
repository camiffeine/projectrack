'''Assignment router with native FastAPI dependency injection (FR-005, FR-008, FR-016, NFR-009)'''

from fastapi import APIRouter, Depends, status
from typing import List, Dict, Any

from auth.auth_bearer import verify_auth, RoleRequired
from models.assignment_model import AssignmentModel
from services.assignment_service import AssignmentService
from dependencies import get_assignment_service, PaginationParams

router = APIRouter(tags=["Assignments"])

@router.post("/assignments/add/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(RoleRequired(2, 3))])
async def add_assignment(
    assignment: AssignmentModel,
    service: AssignmentService = Depends(get_assignment_service)
):
    '''Add an assignment to the database (Professors & Admins - FR-005)'''
    return service.add(assignment)

@router.get("/assignments/get/{assignment_id}", dependencies=[Depends(verify_auth)])
async def get_assignment(
    assignment_id: int,
    service: AssignmentService = Depends(get_assignment_service)
):
    '''Get an assignment from the database (FR-008)'''
    return service.get(assignment_id)

@router.put("/assignments/update/{assignment_id}", dependencies=[Depends(RoleRequired(2, 3))])
async def update_assignment(
    assignment_id: int,
    updates: dict,
    service: AssignmentService = Depends(get_assignment_service)
):
    '''Update an assignment in the database (Professors & Admins)'''
    return service.update(assignment_id, updates)

@router.delete("/assignments/delete/{assignment_id}", dependencies=[Depends(RoleRequired(2, 3))])
async def delete_assignment(
    assignment_id: int,
    service: AssignmentService = Depends(get_assignment_service)
):
    '''Delete an assignment from the database (Professors & Admins)'''
    return service.delete(assignment_id)

@router.get("/assignments/get/", dependencies=[Depends(verify_auth)])
async def get_assignments(
    pagination: PaginationParams = Depends(),
    service: AssignmentService = Depends(get_assignment_service)
):
    '''Get all assignments from the database with pagination (FR-016, NFR-006)'''
    return service.get_all(skip=pagination.skip, limit=pagination.limit)
