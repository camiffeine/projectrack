'''Middleware for verifying authentication with a Bearer token and Role-Based Access Control'''

from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth_handler import verify_token

# Set up the Bearer token scheme
security = HTTPBearer()

async def verify_auth(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    '''Verify the authentication token and return payload'''
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

class RoleRequired:
    '''FastAPI dependency class: verifies the authenticated user has one of the required roles'''
    def __init__(self, *allowed_roles: int):
        self.allowed_roles = allowed_roles

    async def __call__(self, payload: dict = Depends(verify_auth)) -> dict:
        user_role = payload.get("role")
        if user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Insufficient permissions: requires role in {self.allowed_roles}, got {user_role}"
            )
        return payload

def verify_role(*allowed_roles: int):
    '''Factory returning RoleRequired dependency instance for convenience'''
    return RoleRequired(*allowed_roles)

async def get_current_user(payload: dict = Depends(verify_auth)) -> dict:
    '''Extract current user identity from verified JWT payload'''
    return {
        "user_id": payload.get("user_id"),
        "email": payload.get("sub"),
        "role": payload.get("role")
    }
