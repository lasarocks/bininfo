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



from app.core.database import get_db

from app.models.domain.ccsystem import(
    binsCheckout
)



from app.models.schemas.schsystem import(
    CardBinCheckoutAdd,
    CardBinCheckoutAddResponse,
    CardAdd,
    CardRAW
)


from app.exceptions.general import(
    ItemNotFound,
    InternalException,
    InvalidParameters
)



from app.core.checkoutBinlookup import checkoutBinlookup


router = APIRouter()




@router.post(
    '/add',
    status_code=status.HTTP_200_OK
)
def add_bin(
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
            "data": {}
        }
    else:
        return {
            "error": False,
            "message": None,
            "data": temp
        }





@router.get(
    '/find/{card_bin}',
    status_code=status.HTTP_200_OK
)
def has_bin(
    card_bin: str,
    db: Session = Depends(get_db)
):
    try:
        temp = binsCheckout.has_card_bin(session=db, card_bin=card_bin)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON find-bin-checkout -- {err}',
            "data": {}
        }
    else:
        return {
            "error": False,
            "message": None,
            "data": temp or {}
        }






@router.post(
    '/lookup',
    status_code=status.HTTP_200_OK
)
def lookup_bin(
    data_input: Union[CardRAW, CardAdd],
    response: Response,
    db: Session = Depends(get_db)
):
    if isinstance(data_input, CardRAW):
        data = data_input.parse()
    else:
        data = data_input
    try:
        temp = binsCheckout.has_card_bin(session=db, card_bin=data.card_number)
        if not temp:
            temp_checkoutAPI = checkoutBinlookup(timeout=5)
            response_checkoutAPI = temp_checkoutAPI.check_bin(data.raw())
            if response_checkoutAPI:
                data_bin = temp_checkoutAPI.get_request('check_bin').get_extra().get('api_response', {})
                if data_bin:
                    temp_new_bin_data = CardBinCheckoutAdd(**data_bin)
                    temp = binsCheckout.create(session=db, card_bin_data=temp_new_bin_data)
                else:
                    print(f'paypal1-lookup- no databin')
            else:
                print(f'paypal1-lookup no response_processoutAPI')
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON lookup-bin-paypal1 -- {err}',
            "data": {}
        }
    else:
        return {
            "error": False,
            "message": None,
            "data": temp
        }