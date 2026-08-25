'''Role router for handling endpoints'''

from fastapi import APIRouter, HTTPException, Depends

from .base_router import BaseRouter
from auth.auth_bearer import verify_auth, RoleRequired
from models.role_model import RoleModel
from services.role_service import RoleService

# mvc (view/api)

router = APIRouter()
base_router = BaseRouter()
base_router.service = RoleService()  # Dependency injection

# Role CRUD endpoints

@router.post("/roles/add/", tags=["Roles, Users"], status_code=201, dependencies=[Depends(RoleRequired(3))])
async def add_role(role_data: RoleModel):
    '''Add a role to the database (Admin only)'''
    return await base_router.add(role_data)

@router.get("/roles/get/{role_id}", tags=["Roles, Users"], dependencies=[Depends(verify_auth)])
async def get_role(role_id: int):
    '''Get a role from the database'''
    return await base_router.get(role_id)

@router.put("/roles/update/{role_id}", tags=["Roles, Users"], dependencies=[Depends(RoleRequired(3))])
async def update_role(role_id: int, updates: dict):
    '''Update a role in the database (Admin only)'''
    return await base_router.update(role_id, updates)

@router.delete("/roles/delete/{role_id}", tags=["Roles, Users"], dependencies=[Depends(RoleRequired(3))])
async def delete_role(role_id: int):
    '''Delete a role from the database (Admin only)'''
    return await base_router.delete(role_id)

@router.get("/roles/get/", tags=["Roles"], dependencies=[Depends(verify_auth)])
async def get_roles():
    '''Get all the roles from the database'''
    return await base_router.get_all()
