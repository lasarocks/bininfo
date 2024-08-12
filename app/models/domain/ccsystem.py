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



from app.models.schemas.schsystem import(
    CardBinCheckoutAdd,
    CardBinCheckoutAddResponse,
    CardBinPaypal1Add,
    CardBinAdd,
    CardAdd,
    CardBinProcessoutAdd,
    GatewayAdd,
    GatewayAddResponse,
    TransactionAdd,
    TransactionAddResponse,
    CardBinEnduranceAdd,
    CardBinEnduranceAddResponse
)



class binsEndurance(CRUUIDBase, Base):
    __tablename__ = "binsEndurance"
    id = Column(String(36), primary_key=True)
    card_bin = Column(String(255))
    card_brand = Column(String(255))
    card_type = Column(String(255))
    card_category = Column(String(255))
    card_country = Column(String(255))
    card_bank = Column(String(255))
    date_created = Column(DateTime, default=datetime.utcnow())

    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        card_bin_data: CardBinEnduranceAdd
    ):
        response_check_bin = binsEndurance.has_card_bin(session=session, card_bin=card_bin_data.card_bin)
        if not response_check_bin:
            return super().create(session, card_bin_data.dict())
        return response_check_bin
    
    @classmethod
    def has_card_bin(
        cls: Type[Base],
        session: Session,
        card_bin: str
    ):
        if len(card_bin)>=6:
            card_bin_query = card_bin if len(card_bin) == 6 else card_bin[0:6]
            try:
                temp_response = session.query(
                    cls
                ).filter(
                    binsEndurance.card_bin.like(f'{card_bin_query}%')
                ).all()
            except Exception as err:
                print(f'binsEndurance.has_card_bin exp -- {err}')
            else:
                if temp_response:
                    for row in temp_response:
                        if row.card_bin == card_bin[0:len(row.card_bin)]:
                            return row
        return False

    @classmethod
    def has_card_bin2(
        cls: Type[Base],
        session: Session,
        card_bin: str
    ):
        if len(card_bin)>=6:
            card_bin = card_bin if len(card_bin) == 6 else card_bin[0:6]
            try:
                return session.query(
                    cls
                ).filter_by(
                    card_bin=card_bin
                ).one()
            except Exception as err:
                print(f'binsEndurance.has_card_bin exp -- {err}')
        return False



class binsCheckout(CRUUIDBase, Base):
    __tablename__ = "binsCheckout"
    id = Column(String(36), primary_key=True)
    card_bin = Column(String(255))
    card_brand = Column(String(255))
    card_type = Column(String(255))
    card_category = Column(String(255))
    card_country = Column(String(255))
    card_bank = Column(String(255))
    product_id = Column(String(255))
    product_type = Column(String(255))
    date_created = Column(DateTime, default=datetime.utcnow())

    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        card_bin_data: CardBinCheckoutAdd
    ):
        response_check_bin = binsCheckout.has_card_bin(session=session, card_bin=card_bin_data.card_bin)
        if not response_check_bin:
            return super().create(session, card_bin_data.dict())
        return response_check_bin
    
    @classmethod
    def has_card_bin(
        cls: Type[Base],
        session: Session,
        card_bin: str
    ):
        if len(card_bin)>=6:
            card_bin = card_bin if len(card_bin) == 6 else card_bin[0:6]
            try:
                return session.query(
                    cls
                ).filter_by(
                    card_bin=card_bin
                ).one()
            except Exception as err:
                print(f'binsCheckout.has_card_bin exp -- {err}')
        return False




class binsPaypal1(CRUUIDBase, Base):
    __tablename__ = "binsPaypal1"
    id = Column(String(36), primary_key=True)
    card_bin = Column(String(255))
    card_bin_extra = Column(String(255))
    card_brand = Column(String(255))
    card_type = Column(String(255))
    card_country = Column(String(255))
    card_bank = Column(String(255))
    card_networks = Column(String())
    product_types = Column(String())
    status = Column(String())
    date_created = Column(DateTime, default=datetime.utcnow())

    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        card_bin_data: CardBinPaypal1Add
    ):
        temp_card_bin = card_bin_data.card_bin
        temp_card_bin = temp_card_bin[0:6] if len(temp_card_bin)>6 else temp_card_bin
        temp_card_bin_extra = card_bin_data.card_bin
        response_check_bin = binsPaypal1.has_card_bin(session=session, card_bin=temp_card_bin)
        if not response_check_bin:
            card_bin_data_paypal = card_bin_data.dict()
            card_bin_data_paypal.update(
                {
                    'card_bin_extra': temp_card_bin_extra,
                    'card_bin': temp_card_bin
                }
            )
            return super().create(session, card_bin_data_paypal)
        return response_check_bin

    @classmethod
    def has_card_bin(
        cls: Type[Base],
        session: Session,
        card_bin: str
    ):
        if len(card_bin)>=6:
            card_bin_query = card_bin if len(card_bin) == 6 else card_bin[0:6]
            try:
                temp_response = session.query(
                    cls
                ).filter(
                    binsPaypal1.card_bin_extra.like(f'{card_bin_query}%')
                ).all()
            except Exception as err:
                print(f'binsPaypal1.has_card_bin exp -- {err}')
            else:
                if temp_response:
                    for row in temp_response:
                        if row.card_bin_extra == card_bin[0:len(row.card_bin_extra)]:
                            return row
        return False
    
    @classmethod
    def has_card_bin2(
        cls: Type[Base],
        session: Session,
        card_bin: str
    ):
        if len(card_bin)>=6:
            card_bin = card_bin if len(card_bin) == 6 else card_bin[0:6]
            try:
                return session.query(
                    cls
                ).filter(
                    binsPaypal1.card_bin_extra.like(f'{card_bin}%')
                #).filter_by(
                #    card_bin=card_bin
                ).one()
            except Exception as err:
                print(f'binsPaypal1.has_card_bin exp -- {err}')
        return False






class binsProcessout(CRUUIDBase, Base):
    __tablename__ = "binsProcessout"
    id = Column(String(36), primary_key=True)
    card_bin = Column(String(255))
    card_brand = Column(String(255))
    card_type = Column(String(255))
    card_category = Column(String(255))
    card_country = Column(String(255))
    card_bank = Column(String(255))
    card_coscheme = Column(String(255))
    card_preferred_scheme = Column(String(255))
    product_type = Column(String(255))
    date_created = Column(DateTime, default=datetime.utcnow())

    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        card_bin_data: CardBinProcessoutAdd
    ):
        response_check_bin = binsProcessout.has_card_bin(session=session, card_bin=card_bin_data.card_bin)
        if not response_check_bin:
            return super().create(session, card_bin_data.dict())
        return response_check_bin
    
    @classmethod
    def has_card_bin(
        cls: Type[Base],
        session: Session,
        card_bin: str
    ):
        if len(card_bin)>=6:
            card_bin = card_bin if len(card_bin) == 6 else card_bin[0:6]
            try:
                return session.query(
                    cls
                ).filter_by(
                    card_bin=card_bin
                ).one()
            except Exception as err:
                print(f'binsProcessout.has_card_bin exp -- {err}')
        return False






class binners(CRUUIDBase, Base):
    __tablename__ = "binners"
    id = Column(String(36), primary_key=True)
    card_bin = Column(String(255))
    card_bin_extra = Column(String(255))
    card_brand = Column(String(255))
    card_type = Column(String(255))
    card_level = Column(String(255))
    card_country = Column(String(255))
    card_bank = Column(String(255))
    date_created = Column(DateTime, default=datetime.utcnow())

    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        card_bin_data: CardBinAdd
    ):
        response_check_bin = binners.has_card_bin(session=session, card_bin=card_bin_data.card_bin)
        if not response_check_bin:
            return super().create(session, card_bin_data.dict())
        return response_check_bin
    
    @classmethod
    def has_card_bin(
        cls: Type[Base],
        session: Session,
        card_bin: str
    ):
        try:
            return session.query(
                cls
            ).filter_by(
                card_bin=card_bin
            ).one()
        except Exception as err:
            print(f'binners.has_card_bin exp -- {err}')
        return False





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
        response_check_cc = cards.has_card(session=session, card_data=card_data)
        if not response_check_cc or recheck == '1':
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
    def after_create_table(cls, session):
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