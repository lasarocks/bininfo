from pydantic import Field
from datetime import datetime
from app.models.schemas.base import baseSchema

from typing import Optional, List
from uuid import UUID




class binIssuersAdd(baseSchema):
    country: Optional[str] = None
    name: Optional[str] = None
    name_alternative: Optional[str] = None
    



class binIssuersAddResponse(binIssuersAdd):
    id: UUID
    date_created: datetime


class binIssuersListAllResponse(baseSchema):
    data: List[binIssuersAddResponse]



class binnerAdd(baseSchema):
    id_issuer: str
    card_bin: str


class binnerAddResponse(binnerAdd):
    id: UUID
    date_created: datetime
    binIssuers: binIssuersAddResponse


class binnerListAllResponse(baseSchema):
    data: List[binnerAddResponse]