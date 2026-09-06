'''Unit tests for Area 8 & 11: Typed Update Validation and Consistent Response DTOs'''

import pytest
from pydantic import ValidationError

from schemas.class_schemas import ClassUpdate, ClassResponse
from schemas.assignment_schemas import AssignmentUpdate, AssignmentResponse
from schemas.submission_schemas import SubmissionUpdate, SubmissionResponse
from schemas.role_schemas import RoleUpdate, RoleResponse
from schemas.professor_schemas import ProfessorUpdate, ProfessorResponse
from schemas.student_schemas import StudentUpdate, StudentResponse
from schemas.student_assignment_schemas import StudentAssignmentUpdate, StudentAssignmentResponse
from schemas.user_schemas import UserUpdate
from schemas.common_schemas import MutationResponse

def test_class_update_partial_and_validation():
    '''Test that ClassUpdate dumps only set fields and validates constraints'''
    update_partial = ClassUpdate(class_name="Advanced Mathematics")
    dumped = update_partial.model_dump(exclude_unset=True)

    assert dumped == {"class_name": "Advanced Mathematics"}
    assert "professor_id" not in dumped

    # Name too short
    with pytest.raises(ValidationError):
        ClassUpdate(class_name="ab")

def test_assignment_update_partial_and_dump():
    '''Test AssignmentUpdate dumps only provided fields'''
    update = AssignmentUpdate(title="Revised Title", status="Closed")
    dumped = update.model_dump(exclude_unset=True)

    assert dumped == {"title": "Revised Title", "status": "Closed"}
    assert "description" not in dumped
    assert "deadline" not in dumped

def test_submission_update_partial():
    '''Test SubmissionUpdate fields'''
    update = SubmissionUpdate(comment="Updated deliverables link", attachment_url="https://github.com/new-repo")
    dumped = update.model_dump(exclude_unset=True)

    assert dumped == {
        "comment": "Updated deliverables link",
        "attachment_url": "https://github.com/new-repo"
    }
    assert "delivery_type" not in dumped

def test_role_update_and_response_aliasing():
    '''Test RoleUpdate and RoleResponse _id mapping'''
    update = RoleUpdate(description="Updated role description")
    assert update.model_dump(exclude_unset=True) == {"description": "Updated role description"}

    # Response aliasing
    raw_doc = {"_id": 2, "role_name": "Professor", "description": "Academic lead"}
    resp = RoleResponse.model_validate(raw_doc)
    assert resp.role_id == 2
    assert resp.role_name == "Professor"

def test_professor_response_aliasing():
    '''Test ProfessorResponse maps MongoDB _id to professor_id'''
    raw_doc = {"_id": 5, "user_id": 20}
    resp = ProfessorResponse.model_validate(raw_doc)
    assert resp.professor_id == 5
    assert resp.user_id == 20

def test_student_response_aliasing():
    '''Test StudentResponse maps MongoDB _id to student_id'''
    raw_doc = {"_id": 10, "user_id": 30, "class_id": [101, 102]}
    resp = StudentResponse.model_validate(raw_doc)
    assert resp.student_id == 10
    assert resp.user_id == 30
    assert resp.class_id == [101, 102]

def test_student_assignment_response_aliasing():
    '''Test StudentAssignmentResponse maps MongoDB _id to assignment_id'''
    raw_doc = {"_id": 50, "student_id": [10, 11, 12]}
    resp = StudentAssignmentResponse.model_validate(raw_doc)
    assert resp.assignment_id == 50
    assert resp.student_id == [10, 11, 12]

def test_mutation_response_schema():
    '''Test shared MutationResponse model'''
    resp = MutationResponse(msg="Class 101 updated successfully.", entity_id=101)
    assert resp.msg == "Class 101 updated successfully."
    assert resp.entity_id == 101
