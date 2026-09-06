'''Assignment router with student assignment tracking and deliverable queries (FR-005, FR-008, FR-016, NFR-009)'''

from fastapi import APIRouter, Depends, status
from typing import List, Dict, Any

from auth.auth_bearer import verify_auth, RoleRequired
from models.assignment_model import AssignmentModel
from services.assignment_service import AssignmentService
from services.submission_service import SubmissionService
from schemas.assignment_schemas import StudentAssignmentDetailResponse, AssignmentResponse, MaterialAttachmentRequest
from schemas.submission_schemas import SubmissionResponse
from dependencies import get_assignment_service, get_submission_service, PaginationParams
from fastapi import Query

router = APIRouter(tags=["Assignments"])

@router.post("/assignments/add/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(RoleRequired(2, 3))])
async def add_assignment(
    assignment: AssignmentModel,
    service: AssignmentService = Depends(get_assignment_service)
):
    '''Add an assignment to the database (Professors & Admins - FR-005, FR-013)'''
    return service.add(assignment)

@router.get("/assignments/get/{assignment_id}", dependencies=[Depends(verify_auth)])
async def get_assignment(
    assignment_id: int,
    service: AssignmentService = Depends(get_assignment_service)
):
    '''Get an assignment from the database (FR-008)'''
    return service.get(assignment_id)

@router.post(
    "/assignments/{assignment_id}/materials",
    dependencies=[Depends(RoleRequired(2, 3))],
    summary="Add material URLs or guide links to an assignment (FR-013)"
)
async def add_assignment_materials(
    assignment_id: int,
    material_data: MaterialAttachmentRequest,
    service: AssignmentService = Depends(get_assignment_service)
):
    '''Attach materials, guides, or reference links to an assignment (Professors & Admins - FR-013)'''
    return service.add_materials(assignment_id, material_data.materials)

@router.delete(
    "/assignments/{assignment_id}/materials",
    dependencies=[Depends(RoleRequired(2, 3))],
    summary="Remove a material URL from an assignment (FR-013)"
)
async def remove_assignment_material(
    assignment_id: int,
    material_url: str = Query(..., description="URL of the material to remove"),
    service: AssignmentService = Depends(get_assignment_service)
):
    '''Remove a material URL from an assignment (Professors & Admins - FR-013)'''
    return service.remove_material(assignment_id, material_url)

@router.get(
    "/assignments/student/{student_id}",
    response_model=List[StudentAssignmentDetailResponse],
    dependencies=[Depends(verify_auth)],
    summary="Get all assigned projects for a student with submission status (FR-008, FR-016)"
)
@router.get(
    "/students/{student_id}/assignments",
    response_model=List[StudentAssignmentDetailResponse],
    dependencies=[Depends(verify_auth)],
    include_in_schema=False
)
async def get_student_assignments(
    student_id: int,
    service: AssignmentService = Depends(get_assignment_service)
):
    '''Get all assigned projects for a student decorated with live submission and grading status (FR-008, FR-016)'''
    return service.get_student_assignments(student_id)

@router.get(
    "/assignments/{assignment_id}/submissions",
    response_model=List[SubmissionResponse],
    dependencies=[Depends(RoleRequired(2, 3))],
    summary="Get all student submissions for an assignment (Professors & Admins - FR-011)"
)
async def get_assignment_submissions(
    assignment_id: int,
    pagination: PaginationParams = Depends(),
    submission_service: SubmissionService = Depends(get_submission_service)
):
    '''Get all student submissions for an assignment for professor evaluation (FR-011)'''
    return submission_service.get_submissions_by_assignment(
        assignment_id=assignment_id,
        skip=pagination.skip,
        limit=pagination.limit
    )

@router.put("/assignments/update/{assignment_id}", dependencies=[Depends(RoleRequired(2, 3))])
async def update_assignment(
    assignment_id: int,
    updates: dict,
    service: AssignmentService = Depends(get_assignment_service)
):
    '''Update an assignment in the database (Professors & Admins)'''
    return service.update(assignment_id, updates)

@router.delete("/assignments/delete/{assignment_id}", dependencies=[Depends(RoleRequired(2, 3))])
async def delete_assignment(
    assignment_id: int,
    service: AssignmentService = Depends(get_assignment_service)
):
    '''Delete an assignment from the database (Professors & Admins)'''
    return service.delete(assignment_id)

@router.get("/assignments/get/", dependencies=[Depends(verify_auth)])
async def get_assignments(
    pagination: PaginationParams = Depends(),
    service: AssignmentService = Depends(get_assignment_service)
):
    '''Get all assignments from the database with pagination (FR-016, NFR-006)'''
    return service.get_all(skip=pagination.skip, limit=pagination.limit)
