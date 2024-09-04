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



from app.models.schemas.scards import(
    CardAdd,
    CardAddResponse,
    CardRAW,
    CardsListAllResponse,
    c000,
    c000List,
    CardQuery
)




from app.exceptions.general import(
    ItemNotFound,
    InternalException,
    InvalidParameters
)


import json






router = APIRouter()



@router.post(
    '/create',
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
    response = None
    try:
        if source is not None and not data.source:
            data.source = source
        response = cards.create(session=db, card_data=data)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON create-cards -- {err}',
            "data": {}
        }
    return {
        "error": False,
        "message": None,
        "data": CardAddResponse.from_orm(response) or {}
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
        response = cards.list_all(session=db)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON list_all-cards -- {err}',
            "data": {}
        }
    return {
        "error": False,
        "message": None,
        "data": c000List(data=response) or []
    }



@router.post(
    '/list_query',
    status_code=status.HTTP_200_OK
)
def list_query(
    data_query: CardQuery,
    offset: int = 0,
    limit: int = 15,
    db: Session = Depends(get_db)
):
    response = None
    try:
        response = cards.list_cards_query(session=db, data_query=data_query, offset=offset, limit=limit)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON list_query-cards -- {err}',
            "data": {}
        }
    return {
        "error": False,
        "message": None,
        "data": c000List(data=response) or []
    }