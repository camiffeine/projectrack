'''Unit tests for Professor Material Attachments on Assignments (FR-013)'''

import pytest
from unittest.mock import MagicMock

from services.assignment_service import AssignmentService
from exceptions import EntityNotFoundException

def test_add_materials_to_assignment():
    '''Test adding materials/guides to an existing assignment (FR-013)'''
    mock_assignment_repo = MagicMock()
    service = AssignmentService(repo=mock_assignment_repo)

    mock_assignment_repo.exists.return_value = True

    materials = [
        "https://example.com/docs/guide.pdf",
        "https://example.com/slides/week1.pptx"
    ]

    result = service.add_materials(assignment_id=5, materials=materials)

    assert result["assignment_id"] == 5
    assert result["materials"] == materials
    assert "successfully" in result["message"]
    mock_assignment_repo.add_materials.assert_called_once_with(5, materials)

def test_add_materials_assignment_not_found():
    '''Test adding materials to a non-existent assignment raises 404 (FR-013)'''
    mock_assignment_repo = MagicMock()
    service = AssignmentService(repo=mock_assignment_repo)

    mock_assignment_repo.exists.return_value = False

    with pytest.raises(EntityNotFoundException) as excinfo:
        service.add_materials(assignment_id=999, materials=["https://example.com/guide.pdf"])

    assert excinfo.value.status_code == 404
    assert "Assignment" in excinfo.value.detail

def test_remove_material_from_assignment():
    '''Test removing a material URL from an assignment (FR-013)'''
    mock_assignment_repo = MagicMock()
    service = AssignmentService(repo=mock_assignment_repo)

    mock_assignment_repo.exists.return_value = True

    result = service.remove_material(assignment_id=5, material_url="https://example.com/docs/guide.pdf")

    assert result["assignment_id"] == 5
    assert result["material_url"] == "https://example.com/docs/guide.pdf"
    assert "successfully" in result["message"]
    mock_assignment_repo.remove_material.assert_called_once_with(5, "https://example.com/docs/guide.pdf")

def test_remove_material_assignment_not_found():
    '''Test removing a material from a non-existent assignment raises 404 (FR-013)'''
    mock_assignment_repo = MagicMock()
    service = AssignmentService(repo=mock_assignment_repo)

    mock_assignment_repo.exists.return_value = False

    with pytest.raises(EntityNotFoundException) as excinfo:
        service.remove_material(assignment_id=999, material_url="https://example.com/docs/guide.pdf")

    assert excinfo.value.status_code == 404
    assert "Assignment" in excinfo.value.detail

def test_student_assignments_include_materials():
    '''Test that materials appear in student assignment tracking view (FR-008, FR-013, FR-016)'''
    mock_assignment_repo = MagicMock()
    mock_student_repo = MagicMock()
    mock_student_assign_repo = MagicMock()
    mock_submission_repo = MagicMock()

    service = AssignmentService(
        repo=mock_assignment_repo,
        student_repo=mock_student_repo,
        student_assign_repo=mock_student_assign_repo,
        submission_repo=mock_submission_repo
    )

    mock_student_repo.get.return_value = {"_id": 10, "class_id": [101]}
    mock_assignment_repo.get_by_class_ids.return_value = [
        {
            "_id": 1,
            "title": "Algorithms Project",
            "description": "Graph algorithms",
            "class_id": 101,
            "status": "Active",
            "materials": ["https://example.com/rubric.pdf", "https://example.com/starter-code.zip"]
        }
    ]
    mock_student_assign_repo.get_assignments_for_student.return_value = []
    mock_assignment_repo.get_by_ids.return_value = []
    mock_submission_repo.get_by_student_and_assignment.return_value = None

    results = service.get_student_assignments(10)

    assert len(results) == 1
    assert results[0]["assignment_id"] == 1
    assert len(results[0]["materials"]) == 2
    assert "https://example.com/rubric.pdf" in results[0]["materials"]
