'''Student router with native FastAPI dependency injection (NFR-009)'''

from fastapi import APIRouter, Depends, status
from typing import List, Dict, Any

from auth.auth_bearer import verify_auth, RoleRequired
from models.student_model import StudentModel
from services.student_service import StudentService
from dependencies import get_student_service, PaginationParams

router = APIRouter(tags=["Students"])

@router.post("/students/add/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(RoleRequired(3))])
async def add_student(
    student_data: StudentModel,
    service: StudentService = Depends(get_student_service)
):
    '''Add a student to the database (Admin only)'''
    return service.add(student_data)

@router.get("/students/get/{student_id}", dependencies=[Depends(verify_auth)])
async def get_student(
    student_id: int,
    service: StudentService = Depends(get_student_service)
):
    '''Get a student from the database'''
    return service.get(student_id)

@router.put("/students/update/{student_id}", dependencies=[Depends(RoleRequired(3))])
async def update_student(
    student_id: int,
    updates: dict,
    service: StudentService = Depends(get_student_service)
):
    '''Update a student in the database (Admin only)'''
    return service.update(student_id, updates)

@router.delete("/students/delete/{student_id}", dependencies=[Depends(RoleRequired(3))])
async def delete_student(
    student_id: int,
    service: StudentService = Depends(get_student_service)
):
    '''Delete a student from the database (Admin only)'''
    return service.delete(student_id)

@router.get("/students/get/", dependencies=[Depends(verify_auth)])
async def get_students(
    pagination: PaginationParams = Depends(),
    service: StudentService = Depends(get_student_service)
):
    '''Get all students from the database with pagination (NFR-006)'''
    return service.get_all(skip=pagination.skip, limit=pagination.limit)
