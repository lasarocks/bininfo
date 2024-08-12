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
    binsEndurance
)



from app.models.schemas.schsystem import(
    CardBinEnduranceAdd,
    CardBinEnduranceAddResponse,
    CardAdd,
    CardRAW
)


from app.exceptions.general import(
    ItemNotFound,
    InternalException,
    InvalidParameters
)



from app.core.enduranceBinlookup import enduranceBinlookup


router = APIRouter()




@router.post(
    '/add',
    status_code=status.HTTP_200_OK
)
def add_bin(
    data: CardBinEnduranceAdd,
    response: Response,
    db: Session = Depends(get_db)
):
    try:
        temp = binsEndurance.create(session=db, card_bin_data=data)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON add-bin-endurance -- {err}',
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
        temp = binsEndurance.has_card_bin(session=db, card_bin=card_bin)
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
        temp = binsEndurance.has_card_bin(session=db, card_bin=data.card_number)
        if not temp:
            temp_checkoutAPI = enduranceBinlookup(timeout=5)
            response_checkoutAPI = temp_checkoutAPI.check_bin(data.raw())
            if response_checkoutAPI:
                temp_new_bin_data = CardBinEnduranceAdd(**response_checkoutAPI)
                temp = binsEndurance.create(session=db, card_bin_data=temp_new_bin_data)
                if temp:
                    temp = CardBinEnduranceAddResponse.from_orm(temp)
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