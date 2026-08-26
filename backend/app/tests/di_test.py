'''Unit and integration tests for Dependency Injection, Domain Exceptions, and Service Mocking (NFR-009)'''

import pytest
from unittest.mock import MagicMock
from pydantic import SecretStr

from exceptions import (
    AppException,
    EntityNotFoundException,
    EntityAlreadyExistsException,
    BadRequestException,
    ForbiddenException,
    UnauthorizedException
)
from services.user_service import UserService
from services.assignment_service import AssignmentService
from services.class_service import ClassService
from models.user_model import UserModel
from models.assignment_model import AssignmentModel
from models.class_model import ClassModel
from schemas.user_schemas import UserCreate
from dependencies import (
    get_user_service,
    get_assignment_service,
    PaginationParams
)

def test_domain_exception_properties():
    '''Test domain exceptions instantiate with proper status codes and details'''
    e_not_found = EntityNotFoundException("Assignment", 101)
    assert e_not_found.status_code == 404
    assert "Assignment with ID 101 not found" in e_not_found.detail

    e_exists = EntityAlreadyExistsException("User", 42)
    assert e_exists.status_code == 409
    assert "User with ID 42 already exists" in e_exists.detail

    e_bad = BadRequestException("Invalid date range")
    assert e_bad.status_code == 400
    assert e_bad.detail == "Invalid date range"

    e_forbid = ForbiddenException()
    assert e_forbid.status_code == 403

    e_unauth = UnauthorizedException()
    assert e_unauth.status_code == 401

def test_user_service_constructor_injection_and_unit_behavior():
    '''Test UserService with constructor-injected mock repository (pure unit test)'''
    mock_repo = MagicMock()
    mock_role_repo = MagicMock()

    service = UserService(repo=mock_repo, role_repo=mock_role_repo)

    # Test 1: get non-existent raises EntityNotFoundException
    mock_repo.get.return_value = None
    with pytest.raises(EntityNotFoundException) as exc_info:
        service.get(999)
    assert exc_info.value.status_code == 404

    # Test 2: get existing returns document
    mock_repo.get.return_value = {"_id": 1, "first_name": "Alan", "email": "alan@example.com"}
    user_doc = service.get(1)
    assert user_doc["first_name"] == "Alan"

    # Test 3: register duplicate ID raises EntityAlreadyExistsException
    mock_repo.exists.return_value = True
    new_user = UserCreate(
        user_id=1,
        first_name="Alan",
        last_name="Turing",
        email="alan@turing.org",
        password=SecretStr("password123")
    )
    with pytest.raises(EntityAlreadyExistsException):
        service.register(new_user)

    # Test 4: assign role to non-existent user raises EntityNotFoundException
    mock_repo.exists.return_value = False
    with pytest.raises(EntityNotFoundException):
        service.assign_role(999, 1)

def test_assignment_service_constructor_injection():
    '''Test AssignmentService with constructor-injected mock repository'''
    mock_repo = MagicMock()
    service = AssignmentService(repo=mock_repo)

    # 1. Add assignment when ID already exists raises 409
    mock_repo.exists.return_value = True
    assignment = AssignmentModel(
        assignment_id=5,
        title="Data Structures Lab 1",
        description="Implement a binary tree",
        class_id=10
    )
    with pytest.raises(EntityAlreadyExistsException):
        service.add(assignment)

    # 2. Get existing assignment
    mock_repo.exists.return_value = True
    mock_repo.get.return_value = {"_id": 5, "title": "Data Structures Lab 1", "class_id": 10}
    res = service.get(5)
    assert res["title"] == "Data Structures Lab 1"

def test_class_service_constructor_injection():
    '''Test ClassService with constructor-injected mock repository'''
    mock_repo = MagicMock()
    service = ClassService(repo=mock_repo)

    mock_repo.exists.return_value = True
    mock_repo.get.return_value = {"_id": 20, "class_name": "Software Engineering II", "professor_id": 2}
    cls_doc = service.get(20)
    assert cls_doc["class_name"] == "Software Engineering II"

def test_pagination_params_dependency():
    '''Test PaginationParams dependency values'''
    p = PaginationParams(skip=10, limit=25)
    assert p.skip == 10
    assert p.limit == 25
