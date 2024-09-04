from pydantic import Field
from datetime import datetime
from app.models.schemas.base import baseSchema

from typing import Optional, List
from uuid import UUID

from app.models.schemas.scards import(
    CardAddResponse
)

from app.models.schemas.sgateways import(
    GatewayAddResponse
)


class TransactionBase(baseSchema):
    amount: Optional[str] = None
    currency: Optional[str] = None
    status: Optional[str] = None
    response: Optional[str] = None
    response_raw: Optional[str] = None



class TransactionAdd(TransactionBase):
    id_gateway: str
    id_card: str


class TransactionQuery(TransactionBase):
    id_gateway: Optional[str] = None
    id_card: Optional[str] = None



class TransactionCreate(baseSchema):
    id_gateway: str
    id_card: str
    def add(self):
        return TransactionAdd(**{'id_gateway': self.id_gateway,'id_card': self.id_card})




class TransactionAddResponse(TransactionBase):
    id: UUID
    id_gateway: UUID
    id_card: UUID
    date_created: datetime


class TransactionRT(TransactionAddResponse):
    Gateways: GatewayAddResponse


class TransactionsResponse(baseSchema):
    data: List[TransactionRT]




class TransactionRT2(TransactionAddResponse):
    Gateways: GatewayAddResponse
    cards: CardAddResponse


class TransactionsResponse2(baseSchema):
    data: List[TransactionRT2]
