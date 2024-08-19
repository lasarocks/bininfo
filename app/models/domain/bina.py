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

from app.models.schemas.sbinna import(
    binIssuersAdd,
    binIssuersAddResponse,
    binnerAdd,
    binnerAddResponse
)


class binIssuers(CRUUIDBase, Base):
    __tablename__ = "binIssuers"
    id = Column(String(36), primary_key=True)
    country = Column(String(255))
    name = Column(String(255))
    name_alternative = Column(String(255))
    date_created = Column(DateTime, default=datetime.utcnow())
    bins = relationship('binners', backref='binIssuers')

    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        data: binIssuersAdd
    ):
        try:
            return super().create(session, data=data.dict())
        except Exception as err:
            print(f'binIssuers.create exp --- {err}')
        return False



class binNetwork(CRUUIDBase, Base):
    __tablename__ = "binNetwork"
    id = Column(String(36), primary_key=True)
    country = Column(String(255))
    name = Column(String(255))
    name_alternative = Column(String(255))
    date_created = Column(DateTime, default=datetime.utcnow())
    bins = relationship('binners', backref='binIssuers')

    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        data: binIssuersAdd
    ):
        try:
            return super().create(session, data=data.dict())
        except Exception as err:
            print(f'binIssuers.create exp --- {err}')
        return False




class binners(CRUUIDBase, Base):
    __tablename__ = "binners"
    id = Column(String(36), primary_key=True)
    id_issuer = Column(String(36), ForeignKey('binIssuers.id'))
    card_bin = Column(String(255))
    date_created = Column(DateTime, default=datetime.utcnow())

    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        data: binnerAdd
    ):
        response_bin = binners.find_by_card_bin(session=session, card_bin=data.card_bin)
        if not response_bin:
            response_issuer = binIssuers.find_by_id(session=session, id=data.id_issuer)
            if not response_issuer:
                raise InternalException(
                    message=f'Issuer id {data.id_issuer} not found'
                )
            try:
                return super().create(session, data=data.dict())
            except Exception as err:
                print(f'binners.create exp --- {err}')
        return response_bin

    @classmethod
    def find_by_card_bin(
        cls: Type[Base],
        session: Session,
        card_bin: str
    ):
        try:
            return session.query(cls).filter_by(card_bin=card_bin).first()
        except Exception as err:
            print(f'binners.find_by_card_bin exp -- {err}')
        return False