'''Class router for handling endpoints'''

from fastapi import APIRouter, HTTPException, Depends

from .base_router import BaseRouter
from auth.auth_bearer import verify_auth, RoleRequired
from models.class_model import ClassModel
from services.class_service import ClassService

# mvc (view/api)

router = APIRouter()
base_router = BaseRouter()
base_router.service = ClassService()  # Dependency injection

# Class CRUD endpoints

@router.post("/classes/add/", tags=["Classes"], status_code=201, dependencies=[Depends(RoleRequired(2, 3))])
async def add_class(class_data: ClassModel):
    '''Add a class to the database (Professors & Admins - FR-004)'''
    return await base_router.add(class_data)

@router.get("/classes/get/{class_id}", tags=["Classes"], dependencies=[Depends(verify_auth)])
async def get_class(class_id: int):
    '''Get a class from the database'''
    return await base_router.get(class_id)

@router.put("/classes/update/{class_id}", tags=["Classes"], dependencies=[Depends(RoleRequired(2, 3))])
async def update_class(class_id: int, updates: dict):
    '''Update a class in the database (Professors & Admins)'''
    return await base_router.update(class_id, updates)

@router.delete("/classes/delete/{class_id}", tags=["Classes"], dependencies=[Depends(RoleRequired(2, 3))])
async def delete_class(class_id: int):
    '''Delete a class from the database (Professors & Admins)'''
    return await base_router.delete(class_id)

@router.get("/classes/get/", tags=["Classes"], dependencies=[Depends(verify_auth)])
async def get_classes():
    '''Get all the classes from the database'''
    return await base_router.get_all()
