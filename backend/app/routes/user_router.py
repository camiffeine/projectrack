'''User router with native FastAPI dependency injection (FR-001, FR-003, NFR-009)'''

from fastapi import APIRouter, Depends, status
from typing import List

from auth.auth_bearer import verify_auth, RoleRequired
from models.user_model import UserModel
from services.user_service import UserService
from schemas.user_schemas import UserResponse, RoleAssignment
from dependencies import get_user_service, PaginationParams

router = APIRouter(tags=["Users"])

@router.post("/users/add/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(RoleRequired(3))])
async def add_user(
    user: UserModel,
    service: UserService = Depends(get_user_service)
):
    '''Add a user to the database (Admin only)'''
    return service.add(user)

@router.get("/users/get/{user_id}", response_model=UserResponse, dependencies=[Depends(verify_auth)])
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    '''Get a user from the database without sensitive credentials'''
    return service.get(user_id)

@router.put("/users/update/{user_id}", dependencies=[Depends(verify_auth)])
async def update_user(
    user_id: int,
    updates: dict,
    service: UserService = Depends(get_user_service)
):
    '''Update a user in the database'''
    return service.update(user_id, updates)

@router.put("/users/{user_id}/role", dependencies=[Depends(RoleRequired(3))])
async def assign_user_role(
    user_id: int,
    role_data: RoleAssignment,
    service: UserService = Depends(get_user_service)
):
    '''Assign Student (1) or Professor (2) role to a user (Admin only - FR-003)'''
    return service.assign_role(user_id, role_data.role_id)

@router.delete("/users/delete/{user_id}", dependencies=[Depends(RoleRequired(3))])
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    '''Delete a user from the database (Admin only)'''
    return service.delete(user_id)

@router.get("/users/get/", response_model=List[UserResponse], dependencies=[Depends(RoleRequired(3))])
async def get_users(
    pagination: PaginationParams = Depends(),
    service: UserService = Depends(get_user_service)
):
    '''Get all users from the database with pagination (Admin only - NFR-006)'''
    return service.get_all(skip=pagination.skip, limit=pagination.limit)
