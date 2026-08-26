'''Domain exceptions for standardized application error handling (NFR-009)'''

from typing import Any

class AppException(Exception):
    '''Base application exception with HTTP status code and detail message'''
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)

class EntityNotFoundException(AppException):
    '''Raised when an entity by a given ID or key is not found (HTTP 404)'''
    def __init__(self, entity_name: str, entity_id: Any):
        detail = f"{entity_name} with ID {entity_id} not found."
        super().__init__(status_code=404, detail=detail)

class EntityAlreadyExistsException(AppException):
    '''Raised when an entity with a duplicate ID or unique key already exists (HTTP 409)'''
    def __init__(self, entity_name: str, entity_id: Any):
        detail = f"{entity_name} with ID {entity_id} already exists."
        super().__init__(status_code=409, detail=detail)

class BadRequestException(AppException):
    '''Raised when a business validation or payload rule fails (HTTP 400)'''
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class ForbiddenException(AppException):
    '''Raised when user has insufficient role or permissions for an operation (HTTP 403)'''
    def __init__(self, detail: str = "Insufficient permissions to perform this action."):
        super().__init__(status_code=403, detail=detail)

class UnauthorizedException(AppException):
    '''Raised when authentication credentials are missing or invalid (HTTP 401)'''
    def __init__(self, detail: str = "Invalid or expired credentials."):
        super().__init__(status_code=401, detail=detail)
