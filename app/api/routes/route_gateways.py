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



from app.models.domain.gateways import(
    Gateways
)



from app.models.schemas.sgateways import(
    GatewayAdd,
    GatewayAddResponse,
    GatewaysListAllResponse
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
def create_gateway(
    data: GatewayAdd,
    response: Response,
    db: Session = Depends(get_db)
):
    response = None
    try:
        response = Gateways.create(session=db, data=data)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON create-gateway -- {err}',
            "data": {}
        }
    return {
        "error": False,
        "message": None,
        "data": GatewayAddResponse.from_orm(response) or []
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
        response = Gateways.list_all(session=db)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON list_all-gateway -- {err}',
            "data": {}
        }
    return {
        "error": False,
        "message": None,
        "data": GatewaysListAllResponse(data=response) or []
    }