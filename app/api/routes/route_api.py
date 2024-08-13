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

from app.models.domain.ccsystem import(
    binsCheckout,
    binsPaypal1,
    binners,
    cards,
    Gateways
)


from app.models.schemas.schsystem import(
    CardBinCheckoutAdd,
    CardBinCheckoutAddResponse,
    CardBinPaypal1Add,
    CardBinPaypal1AddResponse,
    CardBinAdd,
    CardBinAddResponse,
    CardAdd,
    CardAddResponse,
    GatewayAdd,
    GatewayAddResponse
)


from app.exceptions.general import(
    ItemNotFound,
    InternalException,
    InvalidParameters
)


import random



router = APIRouter()



@router.post(
    '/add',
    status_code=status.HTTP_200_OK
)
def add_gateway(
    data: GatewayAdd,
    response: Response,
    db: Session = Depends(get_db)
):
    try:
        temp = Gateways.create(session=db, data=data)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON add-gateway -- {err}',
            "data": {}
        }
    else:
        return {
            "error": False,
            "message": None,
            "data": GatewayAddResponse.from_orm(temp)
        }




@router.post(
    '/add-bin-checkout',
    status_code=status.HTTP_200_OK
)
def add_cc(
    data: CardBinCheckoutAdd,
    response: Response,
    db: Session = Depends(get_db)
):
    try:
        temp = binsCheckout.create(session=db, card_bin_data=data)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON add-bin-checkout -- {err}',
            "data": []
        }
    else:
        return {
            "error": False,
            "message": None,
            "data": temp
        }




@router.get(
    '/teste',
    status_code=status.HTTP_200_OK
)
def teste(
    request: Request
):
    a = request.app.inst_gdrive
    print(f'caimo no teste ---- valor a: \n{a}\n\nFIM')
    return {
        'gdrive': a
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
    temp_reponse_upload = drive.upload(path_db)
    if temp_reponse_upload:
        return {
            'error': False,
            'data': temp_reponse_upload
        }
    return {
        'error': 'provavelmente'
    }




# @router.get(
#     '/try/cc/{ccnum}/{ccmonth}/{ccyear}/{cvv}',
#     status_code=status.HTTP_200_OK
# )
# def has_cc(
#     ccnum: str,
#     ccmonth: str,
#     ccyear: str,
#     cvv: str,
#     db: Session = Depends(get_db)
# ):
#     addr = 'http://127.0.0.1:8888'
#     pr1 = {'http': addr, 'https': addr}
#     pr1 = {}
#     e = 'vtcwxhzjuczu@wireconnected.com'
#     p = 'vtcwxhzjuczu@wireconnected.com'
#     use_gw = random.choice([maiomenos, coloursComplementsCC])
#     c = use_gw(username=e, password=p, proxies=pr1)
#     c.make_login()
#     xe = c.get_braintree_token()
#     cc = f'{ccnum}|{ccmonth}|{ccyear}|{cvv}'
#     temp = c.try_cc(raw_cc=cc)
#     if temp:
#         return {
#             "data": temp
#         }
#         return temp
#     else:
#         return {
#             "error": True,
#             "message": "No results"
#         }



# @router.post(
#     '/add',
#     status_code=status.HTTP_200_OK
# )
# def add_cc(
#     data: CheckCCRAW,
#     response: Response,
#     db: Session = Depends(get_db)
# ):
#     cc = data.ccraw
#     print(f'nem abre kkk')
#     addr = 'http://127.0.0.1:8888'
#     pr1 = {'http': addr, 'https': addr}
#     pr1 = {}
#     e = 'vtcwxhzjuczu@wireconnected.com'
#     p = 'vtcwxhzjuczu@wireconnected.com'
#     use_gw = random.choice([maiomenos, maiomenos])
#     c = use_gw(username=e, password=p, proxies=pr1)
#     c.make_login()
#     xe = c.get_braintree_token()
#     temp = c.try_cc(raw_cc=cc)
#     if temp:
#         return {
#             "data": temp
#         }
#     return {
#         "response": data.ccraw
#     }
#     return {
#         "num": data.ccnum,
#         "month": data.ccmonth,
#         "year": data.ccyear
#     }





# @router.get(
#     '/random/cpf',
#     status_code=status.HTTP_200_OK
# )
# def random_cpf(
#     db: Session = Depends(get_db)
# ):
#     temp = Registro2.random(session=db)
#     if temp:
#         return {
#             "cels": len(temp.celulares),
#             "ccs": len(temp.cartoes),
#             "data": temp
#         }
#         return temp
#     else:
#         return {
#             "error": True,
#             "message": "No results"
#         }





# @router.get(
#     '/random/cpf/plus',
#     status_code=status.HTTP_200_OK
# )
# def random_cpf(
#     db: Session = Depends(get_db)
# ):
#     temp = Registro2.random_param(session=db)
#     if temp:
#         return {
#             "cels": len(temp.celulares),
#             "ccs": len(temp.cartoes),
#             "data": temp
#         }
#         return temp
#     else:
#         return {
#             "error": True,
#             "message": "No results"
#         }
