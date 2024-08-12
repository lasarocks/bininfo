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

from app.models.domain.ccsystem import(
    cards,
    Gateways,
    Transactions,
    binsPaypal1,
    binsProcessout,
    binsCheckout,
    binsEndurance
)



from app.models.schemas.schsystem import(
    CardAdd,
    CardAddResponse,
    CardBinPaypal1Add,
    CardRAW,
    GatewayAdd,
    GatewayAddResponse,
    TransactionAdd,
    TransactionAddResponse,
    TransactionsResponse,
    TransactionRT2,
    TransactionsResponse2
)


from app.exceptions.general import(
    ItemNotFound,
    InternalException,
    InvalidParameters
)


from app.core.oracle import oracleTryOut
from app.core.braintreeWPmaio import maiomenos

from app.core.strwhatbox import newvbv as stripeVBVEXTERNALbeta1
import json






router = APIRouter()




@router.post(
    '/add',
    status_code=status.HTTP_200_OK
)
def add_card(
    data_input: Union[CardRAW, CardAdd],
    response_page: Response,
    source: str = None,
    db: Session = Depends(get_db)
):
    if isinstance(data_input, CardRAW):
        data = data_input.parse()
    else:
        data = data_input
    try:
        if source is not None and not data.source:
            data.source = source
        temp = cards.create(session=db, card_data=data)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON add-card-cards -- {err}',
            "data": {}
        }
    else:
        return {
            "error": False,
            "message": None,
            "data": temp
        }






@router.post(
    '/check2',
    status_code=status.HTTP_200_OK
)
def check2(
    data_input: CardRAW,
    response_page: Response,
    db: Session = Depends(get_db),
    recheck: str = '0',
    gateway_key: str = 'ORACLE'
):
    data = data_input.parse()
    data_gateway_use = Gateways.find_by_key(session=SessionLocal(), key=gateway_key)
    if not data_gateway_use:
        return {
            "error": True,
            "message": "Gateway key not found",
            "data": None
        }
    data_bin = binsPaypal1.has_card_bin(session=SessionLocal(), card_bin=data.card_number[0:6])
    if recheck == '0':
        temp_check_old = cards.has_card(session=db, card_data=data)
        if temp_check_old:
            return {
                "error": False,
                "message": "Already checked",
                "data": temp_check_old,
                'bin_details': data_bin
            }
    try:
        temp_oracle = oracleTryOut()
        response = temp_oracle.check(data.raw())
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON check cc cards -- {err}',
            "data": {},
            'bin_details': data_bin
        }
    else:
        if response:
            try:
                data.status = response.get('auth_response', '')
                data.source = 'CHKORACLE'
                temp_transaction = None
                temp = cards.create(session=db, card_data=data, recheck=recheck)
                if temp:
                    temp_transaction_item = TransactionAdd(
                        id_gateway=str(data_gateway_use.id),
                        id_card=str(temp.id),
                        amount="5.01",
                        currency="BRL",
                        status=data.status,
                    )
                    temp_transaction = Transactions.create(session=SessionLocal(), data=temp_transaction_item)
            except Exception as err1:
                print(f'EXCEPTION ON CHECK CC --- ADD CARD --- {err1}')
            else:
                if temp:
                    return {
                        "error": False,
                        "message": None,
                        "data": temp,
                        'bin_details': data_bin,
                        'transaction_data': temp_transaction
                    }
                else:
                    print(f'CHECKCC NO TEMP')
    return {
        'error': 'maybe',
        'message': 'n sei',
        'bin_details': data_bin
    }








@router.post(
    '/check',
    status_code=status.HTTP_200_OK
)
def check(
    data_input: CardRAW,
    response_page: Response,
    db: Session = Depends(get_db),
    source: str = None,
    recheck: str = '0',
    gateway_key: str = 'ORACLE'
):
    data = data_input.parse()
    data_gateway_use = Gateways.find_by_key(session=SessionLocal(), key=gateway_key)
    if not data_gateway_use:
        return {
            "error": True,
            "message": "Gateway key not found",
            "data": None
        }
    data_card = cards.find_by_card(session=db, card_data=data)
    if not data_card:
        try:
            if source is not None and not data.source:
                data.source = source
            temp = cards.create(session=db, card_data=data, recheck=recheck)
        except Exception as err:
            print(f'route_card.check exp create card --- {err}')
            return {
                "error": True,
                "message": f'route_card.check exp create card --- {err}',
                "data": None
            }
        else:
            if temp:
                data_card = temp
            else:
                return {
                    "error": True,
                    "message": "Failed create object cards",
                    "data": None
                }
    if recheck == '0':
        temp_check_old = Transactions.find_by_card_id(session=SessionLocal(), id_card=str(data_card.id))
        if temp_check_old:
            return {
                "error": False,
                "message": "Already checked",
                "data": {
                    "transactions": temp_check_old,
                    "card": data_card
                },
                'bin_details': None
            }
    try:
        temp_oracle = oracleTryOut()
        response = temp_oracle.check(data.raw())
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON check cc cards -- {err}',
            "data": {},
            'bin_details': None
        }
    else:
        if response:
            try:
                print(response)
                data.status = response.get('auth_response', '')
                temp_transaction_item = TransactionAdd(
                    id_gateway=str(data_gateway_use.id),
                    id_card=str(data_card.id),
                    amount="5.01",
                    currency="BRL",
                    status=data.status,
                    response=response.get('response', None),
                    response_raw=response.get('response_raw', None),
                )
                temp_transaction = Transactions.create(session=SessionLocal(), data=temp_transaction_item)
            except Exception as err1:
                print(f'EXCEPTION ON CHECK CC --- ADD CARD --- {err1}')
            else:
                if temp_transaction:
                    return {
                        "error": False,
                        "message": None,
                        "data": {
                            "transactions": temp_transaction,
                            "card": data_card
                        },
                        'bin_details': None
                    }
                else:
                    print(f'CHECKCC NO TEMP')
    return {
        'error': 'maybe',
        'message': 'n sei',
        'bin_details': None
    }








@router.post(
    '/check_vbv',
    status_code=status.HTTP_200_OK
)
def check_vbv(
    data_input: CardRAW,
    response_page: Response,
    db: Session = Depends(get_db),
    source: str = None,
    recheck: str = '0',
    gateway_key: str = 'ORACLE'
):
    data = data_input.parse()
    try:
        temp_str_vbv = stripeVBVEXTERNALbeta1()
        response = temp_str_vbv.cvbv(data.raw())
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON check_vbv cards -- {err}',
            "data": {},
            'bin_details': None
        }
    else:
        if response:
            return {
                "error": False,
                "message": None,
                "data": {
                    'vbv': response.get_extra(),
                    'card': data.raw()
                }
            }
    return {
        "error": True,
        "message": "ooops",
        "data": None
    }



@router.post(
    '/check_braintree',
    status_code=status.HTTP_200_OK
)
def check_braintree(
    data_input: CardRAW,
    response_page: Response,
    db: Session = Depends(get_db),
    source: str = None,
    recheck: str = '0',
    gateway_key: str = 'wpbrain1'
):
    data = data_input.parse()
    data_gateway_use = Gateways.find_by_key(session=SessionLocal(), key=gateway_key)
    if not data_gateway_use:
        return {
            "error": True,
            "message": "Gateway key not found",
            "data": None
        }
    data_card = cards.find_by_card(session=db, card_data=data)
    if not data_card:
        try:
            if source is not None and not data.source:
                data.source = source
            temp = cards.create(session=db, card_data=data, recheck=recheck)
        except Exception as err:
            print(f'route_card.check exp create card --- {err}')
            return {
                "error": True,
                "message": f'route_card.check exp create card --- {err}',
                "data": None
            }
        else:
            if temp:
                data_card = temp
            else:
                return {
                    "error": True,
                    "message": "Failed create object cards",
                    "data": None
                }
    if recheck == '0':
        temp_check_old = Transactions.find_by_card_id(session=SessionLocal(), id_card=str(data_card.id))
        if temp_check_old:
            return {
                "error": False,
                "message": "Already checked",
                "data": {
                    "transactions": temp_check_old,
                    "card": data_card
                },
                'bin_details': None
            }
    try:
        temp_maiomenos = maiomenos()
        response = temp_maiomenos.check(data.raw())
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON check cc cards -- {err}',
            "data": {},
            'bin_details': None
        }
    else:
        if response:
            try:
                print(response)
                data.status = response.get('auth_response', '')
                temp_transaction_item = TransactionAdd(
                    id_gateway=str(data_gateway_use.id),
                    id_card=str(data_card.id),
                    amount="0.00",
                    currency="USD",
                    status=data.status,
                    response=response.get('response', None),
                    response_raw=response.get('response_raw', None)
                )
                temp_transaction = Transactions.create(session=SessionLocal(), data=temp_transaction_item)
            except Exception as err1:
                print(f'EXCEPTION ON CHECK CC --- ADD CARD --- {err1}')
            else:
                if temp_transaction:
                    return {
                        "error": False,
                        "message": None,
                        "data": {
                            "transactions": temp_transaction,
                            "card": data_card
                        },
                        'bin_details': None
                    }
                else:
                    print(f'CHECKCC NO TEMP')
    return {
        'error': 'maybe',
        'message': 'n sei',
        'bin_details': None
    }





@router.get(
    '/list_transactions',
    status_code=status.HTTP_200_OK
)
def list_transactions(
    offset: int = 0,
    limit: int = 0,
    db: Session = Depends(get_db)
):
    try:
        temp = TransactionsResponse2(data=Transactions.list_transactions_limit(session=db, offset=offset, limit=limit))
        temp = Transactions.list_transactions_limit(session=db, offset=offset, limit=limit)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON find-bin-endurance -- {err}',
            "data": {}
        }
    else:
        return {
            "error": False,
            "message": None,
            "data": temp or {}
        }







@router.post(
    '/check_multi',
    status_code=status.HTTP_200_OK
)
def check_multi(
    data_input: CardRAW,
    response_page: Response,
    db: Session = Depends(get_db),
    source: str = None,
    recheck: str = '0',
    gateway_key: str = 'ORACLE'
):
    data = data_input.parse()
    data_gateway_use = Gateways.find_by_key(session=SessionLocal(), key=gateway_key)
    if not data_gateway_use:
        return {
            "error": True,
            "message": "Gateway key not found",
            "data": None
        }
    data_card = cards.find_by_card(session=db, card_data=data)
    if not data_card:
        try:
            if source is not None and not data.source:
                data.source = source
            temp = cards.create(session=db, card_data=data, recheck=recheck)
        except Exception as err:
            print(f'route_card.check exp create card --- {err}')
            return {
                "error": True,
                "message": f'route_card.check exp create card --- {err}',
                "data": None
            }
        else:
            if temp:
                data_card = temp
            else:
                return {
                    "error": True,
                    "message": "Failed create object cards",
                    "data": None
                }
    #####TENTAR CARREGAR BIN
    bin_temp_paypal = binsPaypal1.has_card_bin(session=SessionLocal(), card_bin=data_card.card_number)
    bin_temp_checkout = binsCheckout.has_card_bin(session=SessionLocal(), card_bin=data_card.card_bin)
    bin_temp_processout = binsProcessout.has_card_bin(session=SessionLocal(), card_bin=data_card.card_bin)
    bin_temp_endurance = binsEndurance.has_card_bin(session=SessionLocal(), card_bin=data_card.card_number)
    if recheck == '0':
        temp_check_old = Transactions.find_by_card_id(session=SessionLocal(), id_card=str(data_card.id))
        if temp_check_old:
            return {
                "error": False,
                "message": "Already checked",
                "data": {
                    "transactions": TransactionsResponse(data=temp_check_old),
                    "card": data_card
                },
                'bin_details': {
                    'paypal': bin_temp_paypal,
                    'checkout': bin_temp_checkout,
                    'processout': bin_temp_processout,
                    'endurance': bin_temp_endurance
                }
            }
    try:
        temp_oracle = globals()[data_gateway_use.name]()
        response = temp_oracle.check(data.raw())
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON check cc cards -- {err}',
            "data": {},
            'bin_details': {
                'paypal': bin_temp_paypal,
                'checkout': bin_temp_checkout,
                'processout': bin_temp_processout,
                'endurance': bin_temp_endurance
            }
        }
    else:
        if response:
            try:
                print(response)
                data.last_status = response.get('auth_response', '')
                temp_transaction_item = TransactionAdd(
                    id_gateway=str(data_gateway_use.id),
                    id_card=str(data_card.id),
                    amount=response.get("amount", None),
                    currency=response.get("currency", None),
                    status=data.last_status,
                    response=response.get('response', None),
                    response_raw=response.get('response_raw', None),
                )
                temp_transaction = Transactions.create(session=SessionLocal(), data=temp_transaction_item)
                data_card.last_status = data.last_status
                data_card.last_gateway_id = str(data_gateway_use.id)
                print(f'data_card --- {data_card.last_status}')
                recebi_dele = data_card.update(session=db.object_session(data_card))
                print(f'data_card --- {data_card.last_status}')
                print(f'recebi_dele --- {recebi_dele.last_status}')
                db.object_session(data_card).refresh(data_card)
                print(f'data_card DPS REFESH --- {data_card.last_status}')
            except Exception as err1:
                print(f'EXCEPTION ON CHECK CC --- ADD CARD --- {err1}')
            else:
                if temp_transaction:
                    return {
                        "error": False,
                        "message": None,
                        "data": {
                            "transactions": temp_transaction,
                            "card": data_card,
                            "gateway": data_gateway_use
                        },
                        'bin_details': {
                            'paypal': bin_temp_paypal,
                            'checkout': bin_temp_checkout,
                            'processout': bin_temp_processout,
                            'endurance': bin_temp_endurance
                        }
                    }
                else:
                    print(f'CHECKCC NO TEMP')
    return {
        'error': 'maybe',
        'message': 'n sei',
        'bin_details': {
            'paypal': bin_temp_paypal,
            'checkout': bin_temp_checkout,
            'processout': bin_temp_processout,
            'endurance': bin_temp_endurance
        }
    }