'''Class router with native FastAPI dependency injection (FR-004, NFR-009)'''

from fastapi import APIRouter, Depends, status
from typing import List, Dict, Any

from auth.auth_bearer import verify_auth, RoleRequired
from models.class_model import ClassModel
from services.class_service import ClassService
from schemas.class_schemas import ClassEnrollmentRequest, ClassResponse, ClassStudentResponse
from dependencies import get_class_service, PaginationParams

router = APIRouter(tags=["Classes"])

@router.post("/classes/add/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(RoleRequired(2, 3))])
async def add_class(
    class_data: ClassModel,
    service: ClassService = Depends(get_class_service)
):
    '''Add a class to the database (Professors & Admins - FR-004)'''
    return service.add(class_data)

@router.get("/classes/get/{class_id}", dependencies=[Depends(verify_auth)])
async def get_class(
    class_id: int,
    service: ClassService = Depends(get_class_service)
):
    '''Get a class from the database'''
    return service.get(class_id)

@router.post("/classes/{class_id}/students", dependencies=[Depends(RoleRequired(2, 3))], summary="Enroll a student into a class (FR-004)")
async def enroll_student(
    class_id: int,
    enrollment: ClassEnrollmentRequest,
    service: ClassService = Depends(get_class_service)
):
    '''Enroll a student in a class by student ID (Professors & Admins - FR-004)'''
    return service.enroll_student(class_id, enrollment.student_id)

@router.delete("/classes/{class_id}/students/{student_id}", dependencies=[Depends(RoleRequired(2, 3))], summary="Unenroll a student from a class (FR-004)")
async def unenroll_student(
    class_id: int,
    student_id: int,
    service: ClassService = Depends(get_class_service)
):
    '''Unenroll a student from a class by student ID (Professors & Admins - FR-004)'''
    return service.unenroll_student(class_id, student_id)

@router.get(
    "/classes/{class_id}/students",
    response_model=List[ClassStudentResponse],
    dependencies=[Depends(verify_auth)],
    summary="Get all students enrolled in a class (FR-004)"
)
async def get_class_students(
    class_id: int,
    pagination: PaginationParams = Depends(),
    service: ClassService = Depends(get_class_service)
):
    '''Get all students enrolled in a class with pagination (FR-004)'''
    return service.get_enrolled_students(class_id, skip=pagination.skip, limit=pagination.limit)

@router.get(
    "/classes/professor/{professor_id}",
    response_model=List[ClassResponse],
    dependencies=[Depends(verify_auth)],
    summary="Get all classes taught by a professor (FR-004)"
)
async def get_classes_by_professor(
    professor_id: int,
    pagination: PaginationParams = Depends(),
    service: ClassService = Depends(get_class_service)
):
    '''Get all classes taught by a specific professor (FR-004)'''
    return service.get_classes_by_professor(professor_id, skip=pagination.skip, limit=pagination.limit)

@router.put("/classes/update/{class_id}", dependencies=[Depends(RoleRequired(2, 3))])
async def update_class(
    class_id: int,
    updates: dict,
    service: ClassService = Depends(get_class_service)
):
    '''Update a class in the database (Professors & Admins)'''
    return service.update(class_id, updates)

@router.delete("/classes/delete/{class_id}", dependencies=[Depends(RoleRequired(2, 3))])
async def delete_class(
    class_id: int,
    service: ClassService = Depends(get_class_service)
):
    '''Delete a class from the database (Professors & Admins)'''
    return service.delete(class_id)

@router.get("/classes/get/", dependencies=[Depends(verify_auth)])
async def get_classes(
    pagination: PaginationParams = Depends(),
    service: ClassService = Depends(get_class_service)
):
    '''Get all classes from the database with pagination (NFR-006)'''
    return service.get_all(skip=pagination.skip, limit=pagination.limit)
