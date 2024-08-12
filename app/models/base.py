from app.core.database import Base


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
from typing import List, Type, Union


from app.core.database import Base, engine, SessionLocal
from datetime import datetime

import uuid

from app.exceptions.general import(
    ItemNotFound,
    InternalException,
    InvalidParameters
)



class CRUUIDBase:
    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        data: dict
    ) -> Base:
        try:
            obj = cls(**data)
            obj.id = str(uuid.uuid4())
            obj.date_created = datetime.utcnow()
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj
        except Exception as err:
            raise InvalidParameters(
                message=f'CRUUIDBase.create exp --- {err}'
            )
        return False


    @classmethod
    def update(
        cls: Type[Base],
        session: Session
    ):
        try:
            obj = cls()
            session.commit()
            return obj
        except Exception as err:
            print(f'update.CRUUIDBase exp --- {err}')
        return False

    @classmethod
    def list_all(
        cls: Type[Base],
        session: Session
    ) -> List[Base]:
        try:
            return session.query(cls).all()
        except Exception as err:
            raise InternalException(
                message=f'Internal Error listing all'
            )
        return False

    @classmethod
    def __table_cls__(cls, metadata, *args, **kwargs):
        table = Table(cls.__tablename__, Base.metadata, *args)
        if not table.exists(engine):
            table.it_exists = False
            table._wraped = cls
            cls.it_exists = False
        else:
            cls.it_exists = True
        return table

    @classmethod
    def after_create_table(cls, session):
        pass

    @classmethod
    def _after_create(cls, connection):
        temp = cls()
        if temp.it_exists == False:
            session = SessionLocal(bind=connection)
            cls.after_create_table(session=session)

    @event.listens_for(Base.metadata, 'after_create')
    def receive_after_create(target, connection, **kw):
        try:
            t_table = kw.get('tables', [])
            if t_table:
                for itable in t_table:
                    try:
                        temp_obj = itable
                        if hasattr(temp_obj, '_wraped'):
                            if hasattr(temp_obj._wraped, 'it_exists'):
                                try:
                                    temp_obj._wraped._after_create(connection=connection)
                                except Exception as err_aftercreate:
                                    print(f'quebrou _wraped err_aftercreate -- {err_aftercreate}')
                            else:
                                print(f'{temp_obj} nao tem it_exists')
                        else:
                            print(f'{temp_obj} nao tem _wraped---\n====\n{dir(temp_obj)}\n======\n====\n{type(temp_obj)}\n=====')
                    except Exception as err_loading_global:
                        print(f'quebrou err_loading_global --- {err_loading_global}')
            else:
                print(f'sem t_table')
        except Exception as err:
            print(f'BASE receive after exp 1- {err}')

    @classmethod
    def has_id(
        cls: Type[Base],
        session: Session,
        id: str
    ) -> bool:
        try:
            count = session.query(cls).filter_by(id=id).count()
        except Exception as err:
            raise InternalException(
                message=f'Internal Error checking count ID --- {id} --- {err}'
            )
        else:
            return True if count > 0 else False
        return False

    @classmethod
    def find_by_id(
        cls: Type[Base],
        session: Session,
        id: str
    ) -> Union[Base, bool]:
        if cls.has_id(session=session, id=id) == False:
            return False
        try:
            return session.query(cls).filter_by(id=id).first()
        except Exception as err:
            raise InternalException(
                message=f'Internal Error find_by_id ID --- {id} --- {err}'
            )
        return False


