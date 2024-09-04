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

from app.models.base import(
    CRUUIDBase,
    CRUUIDSerial
)

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
    binnerAddResponse,
    CardNetworkAdd,
    CardNetworkAddResponse,
    binNetworkAdd,
    binNetworkAddResponse,
    CardProductAdd,
    CardProductAddResponse,
    binProductAdd,
    binProductAddResponse,
    binInformationAdd,
    binInformationAddResponse
)


class binIssuers(CRUUIDSerial, Base):
    __tablename__ = "binIssuers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    #id = Column(String(36), primary_key=True)
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
            response_check_exists = binIssuers.find_by_name_and_cn(session=session, data=data)
            if not response_check_exists:
                response_check_exists = super().create(session, data=data.dict())
            return response_check_exists
        except Exception as err:
            print(f'binIssuers.create exp --- {err}')
            raise InternalException(
                message=f'Internal Error binIssuers.create {data.dict()} --- {err}'
            )
        return False

    @classmethod
    def find_by_name(
        cls: Type[Base],
        session: Session,
        name: str
    ):
        try:
            return session.query(cls).filter_by(name=name).first()
        except Exception as err:
            raise InternalException(
                message=f'Internal Error find_by_name NAME --- {name} --- {err}'
            )
        return False

    @classmethod
    def find_by_name_and_cn(
        cls: Type[Base],
        session: Session,
        data: binIssuersAdd
    ):
        try:
            return session.query(
                cls
            ).filter(
                binIssuers.name == data.name,
                binIssuers.country == data.country
            ).first()
            #return session.query(cls).filter_by(name=name).first()
        except Exception as err:
            raise InternalException(
                message=f'Internal Error find_by_name_and_cn  --- {data.dict()} --- {err}'
            )
        return False



class CardNetwork(CRUUIDSerial, Base):
    __tablename__ = "CardNetwork"
    id = Column(Integer, primary_key=True, autoincrement=True)
    #id = Column(String(36), primary_key=True)
    name = Column(String(255), unique=True)
    description = Column(String(255))
    date_created = Column(DateTime, default=datetime.utcnow())

    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        data: CardNetworkAdd
    ):
        try:
            response_check_exists = CardNetwork.find_by_name(session=session, name=data.name)
            if not response_check_exists:
                response_check_exists = super().create(session, data=data.dict())
            return response_check_exists
        except Exception as err:
            print(f'CardNetwork.create exp --- {err}')
        return False

    @classmethod
    def find_by_name(
        cls: Type[Base],
        session: Session,
        name: str
    ):
        try:
            return session.query(cls).filter_by(name=name).first()
        except Exception as err:
            raise InternalException(
                message=f'Internal Error find_by_name NAME --- {name} --- {err}'
            )
        return False



class binNetworks(CRUUIDSerial, Base):
    __tablename__ = "binNetworks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    #id = Column(String(36), primary_key=True)
    #id_bin = Column(String(36), ForeignKey('binners.id'))
    id_bin = Column(Integer, ForeignKey('binners.id'))
    #id_network = Column(String(36), ForeignKey('CardNetwork.id'))
    id_network = Column(Integer, ForeignKey('CardNetwork.id'))
    date_created = Column(DateTime, default=datetime.utcnow())
    networks = relationship('CardNetwork', backref='binNetworks')

    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        data: binNetworkAdd
    ):
        response_bin = binners.find_by_id(session=session, id=data.id_bin)
        response_network = CardNetwork.find_by_id(session=session, id=data.id_network)
        if not response_bin or not response_network:
            msg_404 = ''
            if not response_bin:
                msg_404 = f'Bin id {data.id_bin} not found'
            else:
                msg_404 = f'Network id {data.id_network} not found'
            raise InternalException(
                message=msg_404
            )
        try:
            response_check_exists = binNetworks.find_by_relation(session=session, data=data)
            if not response_check_exists:
                return super().create(session, data=data.dict())
        except Exception as err:
            print(f'binNetworks.create exp --- {err}')
        return response_check_exists

    @classmethod
    def find_by_relation(
        cls: Type[Base],
        session: Session,
        data: binNetworkAdd
    ):
        try:
            return session.query(
                cls
            ).filter(
                binNetworks.id_bin == data.id_bin,
                binNetworks.id_network == data.id_network
            ).first()
        except Exception as err:
            raise InternalException(
                message=f'Internal Error find_by_relation --- {err}'
            )
        return False



class CardProduct(CRUUIDSerial, Base):
    __tablename__ = "CardProduct"
    id = Column(Integer, primary_key=True, autoincrement=True)
    #id = Column(String(36), primary_key=True)
    name = Column(String(255), unique=True)
    description = Column(String(255))
    date_created = Column(DateTime, default=datetime.utcnow())

    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        data: CardProductAdd
    ):
        try:
            response_check_exists = CardProduct.find_by_name(session=session, name=data.name)
            if not response_check_exists:
                response_check_exists = super().create(session, data=data.dict())
            return response_check_exists
        except Exception as err:
            print(f'CardProduct.create exp --- {err}')
        return False

    @classmethod
    def find_by_name(
        cls: Type[Base],
        session: Session,
        name: str
    ):
        try:
            return session.query(cls).filter_by(name=name).first()
        except Exception as err:
            raise InternalException(
                message=f'Internal Error find_by_name NAME --- {name} --- {err}'
            )
        return False


class binProducts(CRUUIDSerial, Base):
    __tablename__ = "binProducts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    #id = Column(String(36), primary_key=True)
    #id_bin = Column(String(36), ForeignKey('binners.id'))
    id_bin = Column(Integer, ForeignKey('binners.id'))
    #id_product = Column(String(36), ForeignKey('CardProduct.id'))
    id_product = Column(Integer, ForeignKey('CardProduct.id'))
    date_created = Column(DateTime, default=datetime.utcnow())
    products = relationship('CardProduct', backref='binProducts')

    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        data: binProductAdd
    ):
        response_bin = binners.find_by_id(session=session, id=data.id_bin)
        response_product = CardProduct.find_by_id(session=session, id=data.id_product)
        if not response_bin or not response_product:
            msg_404 = ''
            if not response_bin:
                msg_404 = f'Bin id {data.id_bin} not found'
            else:
                msg_404 = f'Product id {data.id_product} not found'
            raise InternalException(
                message=msg_404
            )
        try:
            response_check_exists = binProducts.find_by_relation(session=session, data=data)
            if not response_check_exists:
                return super().create(session, data=data.dict())
        except Exception as err:
            print(f'binProducts.create exp --- {err}')
        return response_check_exists

    @classmethod
    def find_by_relation(
        cls: Type[Base],
        session: Session,
        data: binProductAdd
    ):
        try:
            return session.query(
                cls
            ).filter(
                binProducts.id_bin == data.id_bin,
                binProducts.id_product == data.id_product
            ).first()
        except Exception as err:
            raise InternalException(
                message=f'Internal Error find_by_relation --- {err}'
            )
        return False



class binInformation(CRUUIDSerial, Base):
    __tablename__ = "binInformation"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_bin = Column(Integer, ForeignKey('binners.id'))
    has_cvc = Column(Boolean)
    cvc_mandatory = Column(Boolean)
    date_created = Column(DateTime, default=datetime.utcnow())

    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        data: binInformationAdd
    ):
        response_bin = binners.find_by_id(session=session, id=data.id_bin)
        if not response_bin:
            msg_404 = f'Bin id {data.id_bin} not found'
            raise InternalException(
                message=msg_404
            )
        try:
            response_check_exists = binInformation.find_by_bin_id(session=session, id_bin=data.id_bin)
            if not response_check_exists:
                response_check_exists = super().create(session, data=data.dict())
            return response_check_exists
        except Exception as err:
            print(f'binInformation.create exp --- {err}')
        return False

    @classmethod
    def find_by_name(
        cls: Type[Base],
        session: Session,
        name: str
    ):
        try:
            return session.query(cls).filter_by(name=name).first()
        except Exception as err:
            raise InternalException(
                message=f'Internal Error find_by_name NAME --- {name} --- {err}'
            )
        return False

    @classmethod
    def find_by_bin_id(
        cls: Type[Base],
        session: Session,
        id_bin: int
    ):
        try:
            return session.query(cls).filter_by(id_bin=id_bin).first()
        except Exception as err:
            raise InternalException(
                message=f'Internal Error find_by_bin_id id_bin --- {id_bin} --- {err}'
            )
        return False



class binners(CRUUIDSerial, Base):
    __tablename__ = "binners"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_issuer = Column(Integer, ForeignKey('binIssuers.id'))
    card_bin = Column(String(255), ForeignKey('cards.card_bin'))
    card_type = Column(String(255))
    card_category = Column(String(255))
    product_category = Column(String(255))
    cvc_mandatory = Column(Boolean)
    date_created = Column(DateTime, default=datetime.utcnow())
    bin_networks = relationship('binNetworks', backref='binners')
    products = relationship('binProducts', backref='binners')
    bin_information = relationship('binInformation', backref='binners')

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

    @classmethod
    def find_bin(
        cls: Type[Base],
        session: Session,
        card_number: str
    ):
        try:
            card_bin_query = card_number[0:6]
            response = session.query(
                cls
            ).filter(
                binners.card_bin.like(f'{card_bin_query}%')
            ).all()
        except Exception as err:
            print(f'binners.find_bin exp -- {err}')
        else:
            if response:
                for row in response:
                    if row.card_bin == card_number[0:len(row.card_bin)]:
                        return row
        return False


