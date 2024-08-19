from datetime import date
from pydantic import Field
from datetime import datetime
from app.models.schemas.base import baseSchema

from typing import Optional, List
from uuid import UUID





class GatewayAdd(baseSchema):
    description: str
    key: str
    name: str
    accepted_brands: Optional[str] = None
    status: Optional[bool] = None




class GatewayAddResponse(GatewayAdd):
    id: UUID
    date_created: datetime


class GatewaysListAllResponse(baseSchema):
    data: List[GatewayAddResponse]