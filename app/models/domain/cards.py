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
    CardQuery
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
    bin_data = relationship('binners', backref='cards')

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
                #cards.card_exp_month == card_data.card_exp_month,
                #cards.card_exp_year == card_data.card_exp_year,
                #cards.card_cvv == card_data.card_cvv
            ).first()
        except Exception as err:
            print(f'cards.find_by_card exp -- {err}')
        return False

    @classmethod
    def list_cards_query(
        cls: Type[Base],
        session: Session,
        data_query: CardQuery,
        offset: int = 0,
        limit: int = 15
    ):
        try:
            select = session.query(cls)
            set_query = data_query.__fields_set__
            if 'last_status' in set_query:
                select = select.filter_by(last_status=data_query.last_status)
            if 'id' in set_query:
                select = select.filter_by(id=data_query.id)
            if 'card_bin' in set_query:
                #select = select.filter_by(card_bin=data_query.card_bin)
                select = select.filter(
                    cards.card_bin.like(f'{data_query.card_bin}%')
                )
            if 'card_number' in set_query:
                select = select.filter_by(card_number=data_query.card_number)
            if 'source' in set_query:
                select = select.filter_by(source=data_query.source)
            return select.offset(offset).limit(limit).all()
        except Exception as err:
            raise InternalException(
                message=f'Internal Error list_transactions_limit offset --- {offset} --- limit --- {limit} --- {err}'
            )
        return False






# class cardInformationType(CRUUIDSerial, Base):
#     __tablename__ = "cardInformationType"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(255), unique=True)
#     description = Column(String(255))



#     id_card = Column(String(36), ForeignKey('cards.id'))
#     has_vbv = Column(Boolean)
#     cvc_mandatory = Column(Boolean)



# class cardInformation(CRUUIDSerial, Base):
#     __tablename__ = "cardInformation"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     id_card = Column(String(36), ForeignKey('cards.id'))
#     id_card_information_type = Column(Integer, ForeignKey('cardInformationType.id'))
#     content = Column(???)
#     #cvc_mandatory = Column(Boolean)
#     date_created = Column(DateTime, default=datetime.utcnow())

#     @classmethod
#     def create(
#         cls: Type[Base],
#         session: Session,
#         data: binInformationAdd
#     ):
#         response_bin = binners.find_by_id(session=session, id=data.id_bin)
#         if not response_bin:
#             msg_404 = f'Bin id {data.id_bin} not found'
#             raise InternalException(
#                 message=msg_404
#             )
#         try:
#             response_check_exists = binInformation.find_by_bin_id(session=session, id_bin=data.id_bin)
#             if not response_check_exists:
#                 response_check_exists = super().create(session, data=data.dict())
#             return response_check_exists
#         except Exception as err:
#             print(f'binInformation.create exp --- {err}')
#         return False

#     @classmethod
#     def find_by_name(
#         cls: Type[Base],
#         session: Session,
#         name: str
#     ):
#         try:
#             return session.query(cls).filter_by(name=name).first()
#         except Exception as err:
#             raise InternalException(
#                 message=f'Internal Error find_by_name NAME --- {name} --- {err}'
#             )
#         return False

#     @classmethod
#     def find_by_bin_id(
#         cls: Type[Base],
#         session: Session,
#         id_bin: int
#     ):
#         try:
#             return session.query(cls).filter_by(id_bin=id_bin).first()
#         except Exception as err:
#             raise InternalException(
#                 message=f'Internal Error find_by_bin_id id_bin --- {id_bin} --- {err}'
#             )
#         return False

