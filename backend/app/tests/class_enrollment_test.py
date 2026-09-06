'''Unit tests for Class Management and Student Enrollment (FR-004)'''

import pytest
from unittest.mock import MagicMock

from services.class_service import ClassService
from exceptions import EntityNotFoundException

def test_enroll_student_success():
    '''Test enrolling an existing student into an existing class (FR-004)'''
    mock_class_repo = MagicMock()
    mock_student_repo = MagicMock()

    service = ClassService(repo=mock_class_repo, student_repo=mock_student_repo)

    mock_class_repo.exists.return_value = True
    mock_student_repo.exists.return_value = True

    result = service.enroll_student(class_id=101, student_id=10)

    assert result["class_id"] == 101
    assert result["student_id"] == 10
    assert "successfully" in result["message"]
    mock_student_repo.enroll_in_class.assert_called_once_with(10, 101)

def test_enroll_student_class_not_found():
    '''Test enrolling into a non-existent class raises 404 (FR-004)'''
    mock_class_repo = MagicMock()
    mock_student_repo = MagicMock()

    service = ClassService(repo=mock_class_repo, student_repo=mock_student_repo)

    mock_class_repo.exists.return_value = False

    with pytest.raises(EntityNotFoundException) as excinfo:
        service.enroll_student(class_id=999, student_id=10)

    assert excinfo.value.status_code == 404
    assert "Class" in excinfo.value.detail

def test_enroll_student_student_not_found():
    '''Test enrolling a non-existent student raises 404 (FR-004)'''
    mock_class_repo = MagicMock()
    mock_student_repo = MagicMock()

    service = ClassService(repo=mock_class_repo, student_repo=mock_student_repo)

    mock_class_repo.exists.return_value = True
    mock_student_repo.exists.return_value = False

    with pytest.raises(EntityNotFoundException) as excinfo:
        service.enroll_student(class_id=101, student_id=999)

    assert excinfo.value.status_code == 404
    assert "Student" in excinfo.value.detail

def test_unenroll_student_success():
    '''Test unenrolling an existing student from a class (FR-004)'''
    mock_class_repo = MagicMock()
    mock_student_repo = MagicMock()

    service = ClassService(repo=mock_class_repo, student_repo=mock_student_repo)

    mock_class_repo.exists.return_value = True
    mock_student_repo.exists.return_value = True

    result = service.unenroll_student(class_id=101, student_id=10)

    assert result["class_id"] == 101
    assert result["student_id"] == 10
    assert "unenrolled" in result["message"]
    mock_student_repo.unenroll_from_class.assert_called_once_with(10, 101)

def test_unenroll_student_class_not_found():
    '''Test unenrolling from non-existent class raises 404'''
    mock_class_repo = MagicMock()
    mock_student_repo = MagicMock()

    service = ClassService(repo=mock_class_repo, student_repo=mock_student_repo)

    mock_class_repo.exists.return_value = False

    with pytest.raises(EntityNotFoundException):
        service.unenroll_student(class_id=999, student_id=10)

def test_unenroll_student_student_not_found():
    '''Test unenrolling non-existent student raises 404'''
    mock_class_repo = MagicMock()
    mock_student_repo = MagicMock()

    service = ClassService(repo=mock_class_repo, student_repo=mock_student_repo)

    mock_class_repo.exists.return_value = True
    mock_student_repo.exists.return_value = False

    with pytest.raises(EntityNotFoundException):
        service.unenroll_student(class_id=101, student_id=999)

def test_get_enrolled_students():
    '''Test retrieving enrolled students for a class (FR-004)'''
    mock_class_repo = MagicMock()
    mock_student_repo = MagicMock()

    service = ClassService(repo=mock_class_repo, student_repo=mock_student_repo)

    mock_class_repo.exists.return_value = True
    mock_student_repo.get_students_by_class.return_value = [
        {"_id": 10, "user_id": 1, "class_id": [101]},
        {"_id": 11, "user_id": 2, "class_id": [101, 102]}
    ]

    roster = service.get_enrolled_students(class_id=101, skip=0, limit=20)

    assert len(roster) == 2
    assert roster[0]["_id"] == 10
    assert roster[1]["_id"] == 11
    mock_student_repo.get_students_by_class.assert_called_once_with(101, skip=0, limit=20)

def test_get_classes_by_professor():
    '''Test retrieving all classes taught by a professor (FR-004)'''
    mock_class_repo = MagicMock()
    mock_student_repo = MagicMock()

    service = ClassService(repo=mock_class_repo, student_repo=mock_student_repo)

    mock_class_repo.get_by_professor.return_value = [
        {"_id": 101, "class_name": "Calculus I", "professor_id": 5},
        {"_id": 102, "class_name": "Linear Algebra", "professor_id": 5}
    ]

    classes = service.get_classes_by_professor(professor_id=5, skip=0, limit=20)

    assert len(classes) == 2
    assert classes[0]["class_name"] == "Calculus I"
    assert classes[1]["professor_id"] == 5
    mock_class_repo.get_by_professor.assert_called_once_with(5, skip=0, limit=20)
