'''Unit and integration tests for Assignment Discovery, Deliverable Submissions, and Professor Feedback (FR-008, FR-010, FR-011, FR-016)'''

import pytest
from unittest.mock import MagicMock
from datetime import datetime

from services.assignment_service import AssignmentService
from services.submission_service import SubmissionService
from schemas.submission_schemas import SubmissionCreate, SubmissionFeedbackRequest
from exceptions import EntityNotFoundException, EntityAlreadyExistsException

def test_student_assignment_aggregation_and_status_tracking():
    '''Test student assignment discovery across enrolled classes and submission status tracking (FR-008, FR-016)'''
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

    # Student 10 is enrolled in class 101 and 102
    mock_student_repo.get.return_value = {"_id": 10, "class_id": [101, 102]}

    # Class 101 has assignment 1; Class 102 has assignment 2
    mock_assignment_repo.get_by_class_ids.return_value = [
        {"_id": 1, "title": "Math Homework 1", "description": "Solve calculus problems", "class_id": 101, "status": "Active"},
        {"_id": 2, "title": "Physics Lab 1", "description": "Pendulum experiment", "class_id": 102, "status": "Active"}
    ]

    # Direct assignments: none
    mock_student_assign_repo.get_assignments_for_student.return_value = []
    mock_assignment_repo.get_by_ids.return_value = []

    # Student has submitted assignment 1, but NOT assignment 2
    def mock_get_sub(student_id, assignment_id):
        if assignment_id == 1:
            return {
                "_id": 501,
                "assignment_id": 1,
                "student_id": 10,
                "status": "FEEDBACK_PROVIDED",
                "attachment_url": "https://github.com/student/calc-hw",
                "grade": 95.0,
                "feedback": "Excellent work!"
            }
        return None

    mock_submission_repo.get_by_student_and_assignment.side_effect = mock_get_sub

    # Execute service
    results = service.get_student_assignments(10)

    assert len(results) == 2

    # Check assignment 1 (with feedback)
    a1 = next(a for a in results if a["assignment_id"] == 1)
    assert a1["submission_status"] == "FEEDBACK_PROVIDED"
    assert a1["grade"] == 95.0
    assert a1["feedback"] == "Excellent work!"
    assert a1["submission_id"] == 501

    # Check assignment 2 (pending)
    a2 = next(a for a in results if a["assignment_id"] == 2)
    assert a2["submission_status"] == "PENDING"
    assert a2["grade"] is None
    assert a2["submission_id"] is None

def test_student_submission_creation_and_validation():
    '''Test student deliverable submission logic (FR-010, FR-012)'''
    mock_submission_repo = MagicMock()
    mock_assignment_repo = MagicMock()

    service = SubmissionService(
        repo=mock_submission_repo,
        assignment_repo=mock_assignment_repo
    )

    # 1. Submission to non-existent assignment raises 404
    mock_submission_repo.exists.return_value = False
    mock_assignment_repo.exists.return_value = False

    sub_data = SubmissionCreate(
        submission_id=1,
        assignment_id=999,
        student_id=10,
        comment="Initial deliverable",
        attachment_url="https://github.com/user/project",
        delivery_type="FINAL"
    )

    with pytest.raises(EntityNotFoundException):
        service.submit_assignment(sub_data)

    # 2. Duplicate submission ID raises 409
    mock_submission_repo.exists.return_value = True
    with pytest.raises(EntityAlreadyExistsException):
        service.submit_assignment(sub_data)

    # 3. Successful submission
    mock_submission_repo.exists.return_value = False
    mock_assignment_repo.exists.return_value = True
    mock_submission_repo.get.return_value = {
        "_id": 1,
        "assignment_id": 5,
        "student_id": 10,
        "status": "SUBMITTED",
        "attachment_url": "https://github.com/user/project",
        "delivery_type": "FINAL"
    }

    sub_valid = SubmissionCreate(
        submission_id=1,
        assignment_id=5,
        student_id=10,
        comment="Final submission",
        attachment_url="https://github.com/user/project",
        delivery_type="FINAL"
    )
    result = service.submit_assignment(sub_valid)
    assert result["_id"] == 1
    assert result["status"] == "SUBMITTED"
    assert result["attachment_url"] == "https://github.com/user/project"

def test_professor_feedback_and_grading():
    '''Test professor feedback and grading workflow (FR-011)'''
    mock_submission_repo = MagicMock()
    service = SubmissionService(repo=mock_submission_repo)

    # 1. Feedback on non-existent submission raises 404
    mock_submission_repo.get.return_value = None
    with pytest.raises(EntityNotFoundException):
        service.provide_feedback(submission_id=999, feedback="Good effort", grade=80.0)

    # 2. Successful feedback
    mock_submission_repo.get.side_effect = [
        {"_id": 100, "status": "SUBMITTED"}, # initial check
        {
            "_id": 100,
            "status": "FEEDBACK_PROVIDED",
            "feedback": "Great implementation of binary search tree.",
            "grade": 98.5,
            "feedback_date": datetime.now()
        } # post-update fetch
    ]

    graded_sub = service.provide_feedback(
        submission_id=100,
        feedback="Great implementation of binary search tree.",
        grade=98.5
    )

    assert graded_sub["status"] == "FEEDBACK_PROVIDED"
    assert graded_sub["grade"] == 98.5
    assert "binary search tree" in graded_sub["feedback"]
    mock_submission_repo.update_feedback.assert_called_once()
