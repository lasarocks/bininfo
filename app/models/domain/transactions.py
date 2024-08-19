from sqlalchemy import(
    Column,
    Integer,
    String,
    ForeignKey,
    text,
    and_,
    or_,
    event
)
from sqlalchemy.schema import Table

from sqlalchemy.orm import Session
from sqlalchemy.types import(
    Date,
    Boolean,
    Time,
    DateTime,
    JSON
)
from typing import List, Type, Union

from sqlalchemy.orm import relationship

from app.core.database import Base, engine, SessionLocal
from datetime import datetime


from sqlalchemy.sql import func

from app.models.base import CRUUIDBase

import uuid


from app.exceptions.general import(
    ItemNotFound,
    InternalException,
    InvalidParameters
)



from app.models.schemas.stransactions import(
    TransactionAdd,
    TransactionCreate,
    TransactionAddResponse,
    TransactionsResponse
)





class Transactions(CRUUIDBase, Base):
    __tablename__ = "Transactions"
    id = Column(String(36), primary_key=True)
    id_gateway = Column(String(36), ForeignKey('Gateways.id'))
    id_card = Column(String(36), ForeignKey('cards.id'))
    #id_card = Column(String(36), nullable=False)
    #id_gateway = Column(String(36), nullable=False)
    amount = Column(String(255))
    currency = Column(String(255))
    status = Column(String(255))
    response = Column(String(255))
    response_raw = Column(String())
    date_created = Column(DateTime, default=datetime.utcnow())


    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        data: TransactionAdd
    ):
        try:
            return super().create(session, data=data.dict())
        except Exception as err:
            print(f'Transactions.create exp --- {err}')
        return False

    @classmethod
    def find_by_card_id(
        cls: Type[Base],
        session: Session,
        id_card: str
    ):
        try:
            return session.query(cls).filter_by(id_card=id_card).all()
        except Exception as err:
            raise InternalException(
                message=f'Internal Error find_by_card_id id_card --- {id_card} --- {err}'
            )
        return False

    @classmethod
    def list_transactions_limit(
        cls: Type[Base],
        session: Session,
        offset: int = 0,
        limit: int = 15
    ):
        try:
            return session.query(cls).offset(offset).limit(limit).all()
        except Exception as err:
            raise InternalException(
                message=f'Internal Error list_transactions_limit offset --- {offset} --- limit --- {limit} --- {err}'
            )
        return False