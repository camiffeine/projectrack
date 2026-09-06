'''Professor router with native FastAPI dependency injection (NFR-009)'''

from fastapi import APIRouter, Depends, status
from typing import List

from auth.auth_bearer import verify_auth, RoleRequired
from models.professor_model import ProfessorModel
from services.professor_service import ProfessorService
from schemas.professor_schemas import ProfessorUpdate, ProfessorResponse
from schemas.common_schemas import MutationResponse
from dependencies import get_professor_service, PaginationParams

router = APIRouter(tags=["Professors"])

@router.post("/professors/add/", response_model=MutationResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RoleRequired(3))])
async def add_professor(
    professor_data: ProfessorModel,
    service: ProfessorService = Depends(get_professor_service)
):
    '''Add a professor to the database (Admin only)'''
    return service.add(professor_data)

@router.get("/professors/get/{professor_id}", response_model=ProfessorResponse, dependencies=[Depends(verify_auth)])
async def get_professor(
    professor_id: int,
    service: ProfessorService = Depends(get_professor_service)
):
    '''Get a professor from the database'''
    return service.get(professor_id)

@router.put("/professors/update/{professor_id}", response_model=MutationResponse, dependencies=[Depends(RoleRequired(3))])
async def update_professor(
    professor_id: int,
    updates: ProfessorUpdate,
    service: ProfessorService = Depends(get_professor_service)
):
    '''Update a professor in the database (Admin only)'''
    return service.update(professor_id, updates.model_dump(exclude_unset=True))

@router.delete("/professors/delete/{professor_id}", response_model=MutationResponse, dependencies=[Depends(RoleRequired(3))])
async def delete_professor(
    professor_id: int,
    service: ProfessorService = Depends(get_professor_service)
):
    '''Delete a professor from the database (Admin only)'''
    return service.delete(professor_id)

@router.get("/professors/get/", response_model=List[ProfessorResponse], dependencies=[Depends(verify_auth)])
async def get_professors(
    pagination: PaginationParams = Depends(),
    service: ProfessorService = Depends(get_professor_service)
):
    '''Get all professors from the database with pagination (NFR-006)'''
    return service.get_all(skip=pagination.skip, limit=pagination.limit)
