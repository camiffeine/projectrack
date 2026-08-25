'''Student Assignment router for handling endpoints'''

from fastapi import APIRouter, Depends

from .base_router import BaseRouter
from auth.auth_bearer import verify_auth, RoleRequired
from models.student_assignment_model import StudentAssignmentModel
from services.student_assignment_service import StudentAssignmentService

# mvc (view/api)

router = APIRouter()
base_router = BaseRouter()
base_router.service = StudentAssignmentService()  # Dependency injection

# Assignment CRUD endpoints

@router.post("/student_assignments/add/", \
             tags=["Student Assignments, Assignments, Students"], status_code=201, dependencies=[Depends(RoleRequired(2, 3))])
async def add_student_assignment(student_assignment: StudentAssignmentModel):
    '''Add a student assignment to the database (Professors & Admins - FR-006)'''
    return await base_router.add(student_assignment)

@router.get("/student_assignments/get/{assignment_id}", \
            tags=["Student Assignments, Assignments, Students"], dependencies=[Depends(verify_auth)])
async def get_student_assignment(assignment_id: int):
    '''Get a student assignment from the database'''
    return await base_router.get(assignment_id)

@router.put("/student_assignments/update/{assignment_id}", \
            tags=["Student Assignments, Assignments, Students"], dependencies=[Depends(RoleRequired(2, 3))])
async def update_student_assignment(assignment_id: int, updates: dict):
    '''Update a student assignment in the database (Professors & Admins)'''
    return await base_router.update(assignment_id, updates)

@router.delete("/student_assignments/delete/{assignment_id}", \
               tags=["Student Assignments, Assignments, Students"], dependencies=[Depends(RoleRequired(2, 3))])
async def delete_student_assignment(assignment_id: int):
    '''Delete a student assignment from the database (Professors & Admins)'''
    return await base_router.delete(assignment_id)

@router.get("/student_assignment", \
            tags=["Student Assignments, Assignments, Students"], dependencies=[Depends(verify_auth)])
async def get_student_assignments():
    '''Get all the student assignments from the database'''
    return await base_router.get_all()
