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



from app.models.schemas.sgateways import(
    GatewayAdd,
    GatewayAddResponse
)



class Gateways(CRUUIDBase, Base):
    __tablename__ = "Gateways"
    id = Column(String(36), primary_key=True)
    description = Column(String(255))
    key = Column(String(255), unique=True)
    name = Column(String())
    accepted_brands = Column(String())
    status = Column(Boolean)
    date_created = Column(DateTime, default=datetime.utcnow())
    transactions = relationship('Transactions', backref='Gateways')

    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        data: GatewayAdd
    ):
        try:
            return super().create(session, data=data.dict())
        except Exception as err:
            print(f'Gateways.create exp --- {err}')
        return False

    @classmethod
    def after_create_table2(cls, session):
        _system_gateway1 = GatewayAdd(
            description = 'OracleCloud',
            key='ORACLE',
            name='oracleTryOut',
            status=True
        )
        Gateways.create(session=session, data=_system_gateway1)

    @classmethod
    def find_by_key(
        cls: Type[Base],
        session: Session,
        key: str
    ):
        try:
            return session.query(cls).filter_by(key=key).first()
        except Exception as err:
            raise InternalException(
                message=f'Internal Error find_by_key KEY --- {key} --- {err}'
            )
        return False