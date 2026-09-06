'''Common schemas shared across domain routers and services'''

from typing import Optional
from pydantic import BaseModel, ConfigDict

class MutationResponse(BaseModel):
    '''Standard response for add, update, and delete mutations'''
    model_config = ConfigDict(extra="ignore")

    msg: str
    entity_id: Optional[int] = None
    id: Optional[str] = None
