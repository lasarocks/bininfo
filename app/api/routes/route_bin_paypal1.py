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
    binsPaypal1
)



from app.models.schemas.schsystem import(
    CardBinPaypal1Add,
    CardBinPaypal1AddResponse,
    CardAdd,
    CardRAW
)


from app.exceptions.general import(
    ItemNotFound,
    InternalException,
    InvalidParameters
)

from app.core.boothpop import boooothPOP

from app.core.block import(
    bootLocker,
    get_boot
)



router = APIRouter()




@router.post(
    '/add',
    status_code=status.HTTP_200_OK
)
def add_bin(
    data: CardBinPaypal1Add,
    response: Response,
    db: Session = Depends(get_db)
):
    try:
        temp = binsPaypal1.create(session=db, card_bin_data=data)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON add-bin-paypal1 -- {err}',
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
        temp = binsPaypal1.has_card_bin(session=db, card_bin=card_bin)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON find-bin-paypal1 -- {err}',
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
    inst_boot: bootLocker = Depends(get_boot),
    db: Session = Depends(get_db)
):
    if isinstance(data_input, CardRAW):
        data = data_input.parse()
    else:
        data = data_input
    try:
        temp = binsPaypal1.has_card_bin(session=db, card_bin=data.card_number)
        if not temp:
            temp_booth = inst_boot
            response_booth = temp_booth.check_bin(data.raw())
            if response_booth:
                data_bin = response_booth.get_extra()
                if data_bin:
                    if data_bin.get('card_bin', False):
                        temp_new_bin_data = CardBinPaypal1Add(**data_bin)
                        temp = binsPaypal1.create(session=db, card_bin_data=temp_new_bin_data)
                    else:
                        print(f'failed invalid card')
                else:
                    print(f'paypal1-lookup- no databin')
            else:
                print(f'paypal1-lookup no response_booth')
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
