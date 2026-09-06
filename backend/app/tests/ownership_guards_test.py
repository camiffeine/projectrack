'''Unit tests for Resource-Level Ownership Authorization Guards (Area 10)'''

import pytest
from unittest.mock import MagicMock
from exceptions import ForbiddenException, EntityNotFoundException
from auth.ownership import (
    verify_user_access,
    verify_user_update_access,
    verify_student_access,
    verify_class_ownership,
    verify_assignment_ownership,
    verify_submission_access,
    get_student_id_for_user,
    get_professor_id_for_user
)

def test_student_cannot_access_other_student_assignments():
    '''Test that Student A cannot access Student B's assignments (Area 10)'''
    mock_student_repo = MagicMock()
    # User 10 is Student 100
    mock_student_repo.get_by_user_id.return_value = {"_id": 100, "user_id": 10}

    with pytest.raises(ForbiddenException) as excinfo:
        verify_student_access(
            target_student_id=200, # Student B
            current_user={"role": 1, "user_id": 10},
            student_repo=mock_student_repo
        )
    assert excinfo.value.status_code == 403
    assert "permission" in excinfo.value.detail

def test_student_can_access_own_assignments():
    '''Test that Student A can access their own assignments (Area 10)'''
    mock_student_repo = MagicMock()
    mock_student_repo.get_by_user_id.return_value = {"_id": 100, "user_id": 10}

    # Should not raise
    verify_student_access(
        target_student_id=100,
        current_user={"role": 1, "user_id": 10},
        student_repo=mock_student_repo
    )

def test_prof_and_admin_bypass_student_restriction():
    '''Test that Professors and Admins can query any student assignments'''
    mock_student_repo = MagicMock()

    # Professor (role 2)
    verify_student_access(target_student_id=200, current_user={"role": 2, "user_id": 5}, student_repo=mock_student_repo)
    # Admin (role 3)
    verify_student_access(target_student_id=200, current_user={"role": 3, "user_id": 1}, student_repo=mock_student_repo)
    # Neither should call get_by_user_id
    mock_student_repo.get_by_user_id.assert_not_called()

def test_professor_cannot_modify_unowned_class():
    '''Test that Professor X cannot modify a class taught by Professor Y (Area 10)'''
    mock_class_repo = MagicMock()
    mock_prof_repo = MagicMock()

    # Professor user 5 is Professor 50
    mock_prof_repo.get_by_user_id.return_value = {"_id": 50, "user_id": 5}
    # Class 101 belongs to Professor 99
    mock_class_repo.get.return_value = {"_id": 101, "class_name": "Physics", "professor_id": 99}

    with pytest.raises(ForbiddenException) as excinfo:
        verify_class_ownership(
            class_id=101,
            current_user={"role": 2, "user_id": 5},
            class_repo=mock_class_repo,
            prof_repo=mock_prof_repo
        )
    assert excinfo.value.status_code == 403
    assert "do not teach" in excinfo.value.detail

def test_professor_can_modify_own_class():
    '''Test that Professor X can modify their own class (Area 10)'''
    mock_class_repo = MagicMock()
    mock_prof_repo = MagicMock()

    mock_prof_repo.get_by_user_id.return_value = {"_id": 50, "user_id": 5}
    mock_class_repo.get.return_value = {"_id": 101, "class_name": "Physics", "professor_id": 50}

    # Should not raise
    verify_class_ownership(
        class_id=101,
        current_user={"role": 2, "user_id": 5},
        class_repo=mock_class_repo,
        prof_repo=mock_prof_repo
    )

def test_admin_can_modify_any_class():
    '''Test that Admin bypasses class ownership checks'''
    mock_class_repo = MagicMock()
    mock_prof_repo = MagicMock()

    verify_class_ownership(
        class_id=101,
        current_user={"role": 3, "user_id": 1},
        class_repo=mock_class_repo,
        prof_repo=mock_prof_repo
    )
    mock_class_repo.get.assert_not_called()

def test_student_cannot_access_other_submission():
    '''Test that Student A cannot view or update Student B's submission (Area 10)'''
    mock_submission_repo = MagicMock()
    mock_student_repo = MagicMock()

    mock_student_repo.get_by_user_id.return_value = {"_id": 100, "user_id": 10}
    # Submission belongs to student 200
    mock_submission_repo.get.return_value = {"_id": 501, "student_id": 200, "assignment_id": 1}

    with pytest.raises(ForbiddenException) as excinfo:
        verify_submission_access(
            submission_id=501,
            current_user={"role": 1, "user_id": 10},
            submission_repo=mock_submission_repo,
            student_repo=mock_student_repo
        )
    assert excinfo.value.status_code == 403

def test_student_can_access_own_submission():
    '''Test that Student A can view/update their own submission'''
    mock_submission_repo = MagicMock()
    mock_student_repo = MagicMock()

    mock_student_repo.get_by_user_id.return_value = {"_id": 100, "user_id": 10}
    mock_submission_repo.get.return_value = {"_id": 501, "student_id": 100, "assignment_id": 1}

    verify_submission_access(
        submission_id=501,
        current_user={"role": 1, "user_id": 10},
        submission_repo=mock_submission_repo,
        student_repo=mock_student_repo
    )

def test_user_profile_access_and_update_guards():
    '''Test user profile view and update authorization logic'''
    # Student 1 cannot view User 2
    with pytest.raises(ForbiddenException):
        verify_user_access(target_user_id=2, current_user={"role": 1, "user_id": 1})

    # Student 1 can view User 1
    verify_user_access(target_user_id=1, current_user={"role": 1, "user_id": 1})

    # Professor 5 can view User 2
    verify_user_access(target_user_id=2, current_user={"role": 2, "user_id": 5})

    # User 1 cannot update User 2
    with pytest.raises(ForbiddenException):
        verify_user_update_access(target_user_id=2, current_user={"role": 1, "user_id": 1})

    # User 1 can update User 1
    verify_user_update_access(target_user_id=1, current_user={"role": 1, "user_id": 1})

    # Admin can update User 2
    verify_user_update_access(target_user_id=2, current_user={"role": 3, "user_id": 99})
