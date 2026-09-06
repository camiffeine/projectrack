'''Student Assignment router with native FastAPI dependency injection (FR-006, NFR-009)'''

from fastapi import APIRouter, Depends, status
from typing import List

from auth.auth_bearer import verify_auth, RoleRequired
from models.student_assignment_model import StudentAssignmentModel
from services.student_assignment_service import StudentAssignmentService
from schemas.student_assignment_schemas import StudentAssignmentUpdate, StudentAssignmentResponse
from schemas.common_schemas import MutationResponse
from dependencies import get_student_assignment_service, PaginationParams

router = APIRouter(tags=["Student Assignments"])

@router.post("/student_assignments/add/", response_model=MutationResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RoleRequired(2, 3))])
async def add_student_assignment(
    student_assignment: StudentAssignmentModel,
    service: StudentAssignmentService = Depends(get_student_assignment_service)
):
    '''Add a student assignment to the database (Professors & Admins - FR-006)'''
    return service.add(student_assignment)

@router.get("/student_assignments/get/{assignment_id}", response_model=StudentAssignmentResponse, dependencies=[Depends(verify_auth)])
async def get_student_assignment(
    assignment_id: int,
    service: StudentAssignmentService = Depends(get_student_assignment_service)
):
    '''Get a student assignment from the database'''
    return service.get(assignment_id)

@router.put("/student_assignments/update/{assignment_id}", response_model=MutationResponse, dependencies=[Depends(RoleRequired(2, 3))])
async def update_student_assignment(
    assignment_id: int,
    updates: StudentAssignmentUpdate,
    service: StudentAssignmentService = Depends(get_student_assignment_service)
):
    '''Update a student assignment in the database (Professors & Admins)'''
    return service.update(assignment_id, updates.model_dump(exclude_unset=True))

@router.delete("/student_assignments/delete/{assignment_id}", response_model=MutationResponse, dependencies=[Depends(RoleRequired(2, 3))])
async def delete_student_assignment(
    assignment_id: int,
    service: StudentAssignmentService = Depends(get_student_assignment_service)
):
    '''Delete a student assignment from the database (Professors & Admins)'''
    return service.delete(assignment_id)

@router.get("/student_assignments/get/", response_model=List[StudentAssignmentResponse], dependencies=[Depends(verify_auth)])
@router.get("/student_assignment", response_model=List[StudentAssignmentResponse], dependencies=[Depends(verify_auth)], include_in_schema=False)
async def get_student_assignments(
    pagination: PaginationParams = Depends(),
    service: StudentAssignmentService = Depends(get_student_assignment_service)
):
    '''Get all student assignments from the database with pagination (NFR-006)'''
    return service.get_all(skip=pagination.skip, limit=pagination.limit)
