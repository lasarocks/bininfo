from pydantic import Field
from datetime import datetime
from app.models.schemas.base import baseSchema

from typing import Optional, List
from uuid import UUID




class baseAPIResponse(baseSchema):
    error: bool
    message: Optional[str] = None
