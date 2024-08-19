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



from app.models.schemas.scards import(
    CardAdd,
    CardAddResponse,
    CardRAW,
)


class cards(CRUUIDBase, Base):
    __tablename__ = "cards"
    id = Column(String(36), primary_key=True)
    card_bin = Column(String(255))
    card_number = Column(String(255))
    card_exp_month = Column(String(255))
    card_exp_year = Column(String(255))
    card_cvv = Column(String(255))
    last_status = Column(String(255))
    last_gateway_id = Column(String(36), ForeignKey('Gateways.id'))
    source = Column(String(255))
    transactions = relationship('Transactions', backref='cards')
    date_created = Column(DateTime, default=datetime.utcnow())

    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        card_data: CardAdd,
        recheck='0'
    ):
        response_check_cc = cards.find_by_card(session=session, card_data=card_data)
        if not response_check_cc:
            if card_data.card_bin is None:
                card_data.card_bin = card_data.card_number[0:6]
            return super().create(session, card_data.dict())
        return response_check_cc

    @classmethod
    def has_card(
        cls: Type[Base],
        session: Session,
        card_data: CardAdd
    ):
        try:
            return session.query(
                cls
            ).filter(
                #cards.card_bin == card_data.card_bin,
                cards.card_number == card_data.card_number,
                cards.card_exp_month == card_data.card_exp_month,
                cards.card_exp_year == card_data.card_exp_year,
                cards.card_cvv == card_data.card_cvv
            ).all()
        except Exception as err:
            print(f'cards.has_card exp -- {err}')
        return False

    @classmethod
    def find_by_card(
        cls: Type[Base],
        session: Session,
        card_data: CardAdd
    ):
        try:
            return session.query(
                cls
            ).filter(
                #cards.card_bin == card_data.card_bin,
                cards.card_number == card_data.card_number,
                cards.card_exp_month == card_data.card_exp_month,
                cards.card_exp_year == card_data.card_exp_year,
                cards.card_cvv == card_data.card_cvv
            ).one()
        except Exception as err:
            print(f'cards.find_by_card exp -- {err}')
        return False