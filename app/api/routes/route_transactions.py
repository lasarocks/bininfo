import os
from typing import List, Union
from sqlalchemy.orm import Session
from fastapi import(
    Depends,
    Response,
    status,
    APIRouter
)
from fastapi.responses import JSONResponse



from app.core.database import get_db, SessionLocal


from app.models.domain.cards import(
    cards
)



from app.models.domain.gateways import(
    Gateways
)

from app.models.domain.transactions import(
    Transactions
)


from app.models.schemas.scards import(
    CardAdd,
    CardAddResponse,
    CardRAW,
)

from app.models.schemas.sgateways import(
    GatewayAdd,
    GatewayAddResponse
)

from app.models.schemas.stransactions import(
    TransactionAdd,
    TransactionCreate,
    TransactionAddResponse,
    TransactionsResponse,
    TransactionsResponse2,
    TransactionBase,
    TransactionQuery
)


from app.exceptions.general import(
    ItemNotFound,
    InternalException,
    InvalidParameters
)


#from app.core.oracle import oracleTryOut
#from app.core.braintreeWPmaio import maiomenos

#from app.core.strwhatbox import newvbv as stripeVBVEXTERNALbeta1
import json






router = APIRouter()




@router.post(
    '/create',
    status_code=status.HTTP_200_OK
)
def create_transaction(
    data_input: TransactionCreate,
    response_page: Response,
    source: str = None,
    recheck: str = '0',
    db: Session = Depends(get_db)
):
    data_gateway_use = Gateways.find_by_id(session=SessionLocal(), id=data_input.id_gateway)
    if not data_gateway_use:
        return {
            "error": True,
            "message": "Gateway not found",
            "data": None
        }
    data_card = cards.find_by_id(session=db, id=data_input.id_card)
    if not data_card:
        return {
            "error": True,
            "message": "Card not found",
            "data": None
        }
    if recheck == '0':
        data_old_transaction = Transactions.find_by_card_id(session=db, id_card=data_input.id_card)
        if data_old_transaction:
            return {
                "error": False,
                "message": "Already checked",
                "data": {
                    "transactions": TransactionsResponse(data=data_old_transaction),
                    "card": data_card
                },
                'bin_details': None
            }
    try:
        response = Transactions.create(session=db, data=data_input.add())
    except Exception as err1:
        print(f'EXCEPTION ON create transaction --- {err1}')
    else:
        if response:
            return {
                "error": False,
                "message": None,
                "data": {
                    "transactions": response,
                    "card": data_card,
                    "gateway": data_gateway_use
                }
            }



@router.get(
    '/list',
    status_code=status.HTTP_200_OK
)
def list(
    db: Session = Depends(get_db)
):
    response = None
    try:
        response = Transactions.list_all(session=db)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON list_all-transactions -- {err}',
            "data": {}
        }
    return {
        "error": False,
        "message": None,
        "data": TransactionsResponse2(data=response) or []
    }




@router.patch(
    '/pay/{id}',
    status_code=status.HTTP_200_OK
)
def pay(
    id: str,
    data_payment: TransactionBase,
    db: Session = Depends(get_db)
):
    response = None
    try:
        response = Transactions.find_by_id(session=db, id=id)
        if response:
            response.amount = data_payment.amount
            response.currency = data_payment.currency
            response.status = data_payment.status
            response.response = data_payment.response
            response.response_raw = data_payment.response_raw
            response.cards.last_status = data_payment.status
            response.cards.last_gateway_id = response.id_gateway
            rs = response.update(session=db)
            return {
                'error': False,
                'message': None,
                'data': TransactionAddResponse.from_orm(response)
            }
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON pay-transactions -- {err}',
            "data": {}
        }
    return {
        "error": False,
        "message": None,
        "data": None
    }



@router.post(
    '/list_query',
    status_code=status.HTTP_200_OK
)
def list_query(
    data_query: TransactionQuery,
    offset: int = 0,
    limit: int = 15,
    db: Session = Depends(get_db)
):
    response = None
    try:
        response = Transactions.list_transactions_limit(session=db, data_query=data_query, offset=offset, limit=limit)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON list_all-transactions -- {err}',
            "data": {}
        }
    return {
        "error": False,
        "message": None,
        "data": TransactionsResponse2(data=response) or []
    }