'''User router for handling endpoints'''

from fastapi import APIRouter, HTTPException, Depends
from typing import List

from .base_router import BaseRouter
from auth.auth_bearer import verify_auth, RoleRequired
from models.user_model import UserModel
from services.user_service import UserService
from schemas.user_schemas import UserResponse, RoleAssignment

# mvc (view/api)

router = APIRouter()
base_router = BaseRouter()
user_service = UserService()
base_router.service = user_service  # Dependency injection

# User CRUD endpoints

@router.post("/users/add/", tags=["Users"], status_code=201, dependencies=[Depends(RoleRequired(3))])
async def add_user(user: UserModel):
    '''Add a user to the database (Admin only)'''
    return await base_router.add(user)

@router.get("/users/get/{user_id}", tags=["Users"], response_model=UserResponse, dependencies=[Depends(verify_auth)])
async def get_user(user_id: int):
    '''Get a user from the database without sensitive credentials'''
    return await base_router.get(user_id)

@router.put("/users/update/{user_id}", tags=["Users"], dependencies=[Depends(verify_auth)])
async def update_user(user_id: int, updates: dict):
    '''Update a user in the database'''
    return await base_router.update(user_id, updates)

@router.put("/users/{user_id}/role", tags=["Users"], dependencies=[Depends(RoleRequired(3))])
async def assign_user_role(user_id: int, role_data: RoleAssignment):
    '''Assign Student (1) or Professor (2) role to a user (Admin only - FR-003)'''
    result = user_service.assign_role(user_id, role_data.role_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.delete("/users/delete/{user_id}", tags=["Users"], dependencies=[Depends(RoleRequired(3))])
async def delete_user(user_id: int):
    '''Delete a user from the database (Admin only)'''
    return await base_router.delete(user_id)

@router.get("/users/get/", tags=["Users"], response_model=List[UserResponse], dependencies=[Depends(RoleRequired(3))])
async def get_users():
    '''Get all the users from the database (Admin only)'''
    return await base_router.get_all()
