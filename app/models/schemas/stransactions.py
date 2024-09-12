from pydantic import Field, validator
from datetime import datetime, date
from app.models.schemas.base import baseSchema

from typing import Optional, List
from uuid import UUID

from app.models.schemas.scards import(
    CardAddResponse,
    c000
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
    date_start: Optional[str] = Field(
        title='Minimum Date',
        description='Set minimum query value datetime',
        examples=[
            'MM-DD-YYYY HH:MM:SS'
        ],
        default=None
    )
    date_end: Optional[str] = Field(
        title='Maximum Date',
        description='Set maximum query value datetime',
        examples=[
            'MM-DD-YYYY HH:MM:SS'
        ]
    )
    @validator('date_start')
    def parse_date_start(cls, v):
        return datetime.strptime(v, '%m-%d-%Y %H:%M:%S')






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
    cards: c000


class TransactionsResponse2(baseSchema):
    data: List[TransactionRT2]
