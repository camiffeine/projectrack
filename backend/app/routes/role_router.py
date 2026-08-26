'''Role router with native FastAPI dependency injection (NFR-009)'''

from fastapi import APIRouter, Depends, status
from typing import List, Dict, Any

from auth.auth_bearer import verify_auth, RoleRequired
from models.role_model import RoleModel
from services.role_service import RoleService
from dependencies import get_role_service, PaginationParams

router = APIRouter(tags=["Roles"])

@router.post("/roles/add/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(RoleRequired(3))])
async def add_role(
    role_data: RoleModel,
    service: RoleService = Depends(get_role_service)
):
    '''Add a role to the database (Admin only)'''
    return service.add(role_data)

@router.get("/roles/get/{role_id}", dependencies=[Depends(verify_auth)])
async def get_role(
    role_id: int,
    service: RoleService = Depends(get_role_service)
):
    '''Get a role from the database'''
    return service.get(role_id)

@router.put("/roles/update/{role_id}", dependencies=[Depends(RoleRequired(3))])
async def update_role(
    role_id: int,
    updates: dict,
    service: RoleService = Depends(get_role_service)
):
    '''Update a role in the database (Admin only)'''
    return service.update(role_id, updates)

@router.delete("/roles/delete/{role_id}", dependencies=[Depends(RoleRequired(3))])
async def delete_role(
    role_id: int,
    service: RoleService = Depends(get_role_service)
):
    '''Delete a role from the database (Admin only)'''
    return service.delete(role_id)

@router.get("/roles/get/", dependencies=[Depends(verify_auth)])
async def get_roles(
    pagination: PaginationParams = Depends(),
    service: RoleService = Depends(get_role_service)
):
    '''Get all roles from the database with pagination (NFR-006)'''
    return service.get_all(skip=pagination.skip, limit=pagination.limit)
