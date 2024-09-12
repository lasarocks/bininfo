import os
from typing import List
from sqlalchemy.orm import Session
from fastapi import(
    Depends,
    Response,
    status,
    APIRouter,
    Request
)
from fastapi.responses import JSONResponse



from app.core.database import get_db


from app.models.domain.cards import(
    cards
)



from app.models.domain.gateways import(
    Gateways
)

from app.models.domain.transactions import(
    Transactions
)


from app.models.domain.bina import(
    binIssuers,
    binners,
    CardNetwork,
    binNetworks,
    CardProduct,
    binProducts,
    binInformation
)

from app.models.schemas.sapi import(
    baseAPIResponse
)
from sqlalchemy import func

from sqlalchemy.sql.expression import literal


from app.exceptions.general import(
    ItemNotFound,
    InternalException,
    InvalidParameters
)
from app.models.schemas.base import baseSchema
from typing import Optional, List


import random



class sts1(baseSchema):
    TOTAL: Optional[int] = None
    tabela: Optional[str] = None



class stt(baseSchema):
    data: List[sts1]




router = APIRouter()







@router.get(
    '/list',
    status_code=status.HTTP_200_OK
)
def list(
    db: Session = Depends(get_db)
):
    qcards_count = db.query(func.count(cards.id).label('TOTAL')).scalar_subquery()
    qbinners_count = db.query(func.count(binners.id).label('TOTAL')).scalar_subquery()
    qbinIssuers_count = db.query(func.count(binIssuers.id).label('TOTAL')).scalar_subquery()
    qCardNetwork_count = db.query(func.count(CardNetwork.id).label('TOTAL')).scalar_subquery()
    qbinNetworks_count = db.query(func.count(binNetworks.id).label('TOTAL')).scalar_subquery()
    qCardProduct_count = db.query(func.count(CardProduct.id).label('TOTAL')).scalar_subquery()
    qbinProducts_count = db.query(func.count(binProducts.id).label('TOTAL')).scalar_subquery()
    qbinInformation_count = db.query(func.count(binInformation.id).label('TOTAL')).scalar_subquery()
    qGateways_count = db.query(func.count(Gateways.id).label('TOTAL')).scalar_subquery()
    qTransactions_count = db.query(func.count(Transactions.id).label('TOTAL')).scalar_subquery()
    try:
        response = db.query(
            qcards_count.label('TOTAL'), literal('cards').label('tabela')
        ).union_all(
            db.query(qbinners_count, literal('binners').label('tabela')),
            db.query(qbinIssuers_count, literal('binIssuers').label('tabela')),
            db.query(qCardNetwork_count, literal('CardNetwork').label('tabela')),
            db.query(qbinNetworks_count, literal('binNetworks').label('tabela')),
            db.query(qCardProduct_count, literal('CardProduct').label('tabela')),
            db.query(qbinProducts_count, literal('binProducts').label('tabela')),
            db.query(qbinInformation_count, literal('binInformation').label('tabela')),
            db.query(qGateways_count, literal('Gateways').label('tabela')),
            db.query(qTransactions_count, literal('Transactions').label('tabela')),
        ).all()
        if response:
            return {
                "error": False,
                "message": None,
                "data": stt(data=response)
            }
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON list_all-transactions -- {err}',
            "data": {}
        }
    return {
        "error": False,
        "message": None,
        "data": []
    }







@router.get(
    '/upload_db',
    status_code=status.HTTP_200_OK
)
def upload_db(
    request: Request
):
    drive = request.app.inst_gdrive
    path_db = request.app.path_database
    temp_reponse_upload = drive.update_remote_db(DB_PATH=path_db, DB_NAME='')
    if temp_reponse_upload:
        return {
            'error': False,
            'data': temp_reponse_upload
        }
    return {
        'error': 'provavelmente'
    }