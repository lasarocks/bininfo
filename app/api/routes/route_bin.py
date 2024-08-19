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



from app.models.domain.bina import(
    binIssuers,
    binners
)



from app.models.schemas.sbinna import(
    binIssuersAdd,
    binIssuersAddResponse,
    binnerAdd,
    binnerAddResponse,
    binIssuersListAllResponse,
    binnerListAllResponse
)




from app.exceptions.general import(
    ItemNotFound,
    InternalException,
    InvalidParameters
)


import json






router = APIRouter()



@router.post(
    '/create_issuer',
    status_code=status.HTTP_200_OK
)
def create_issuer(
    data: binIssuersAdd,
    response: Response,
    db: Session = Depends(get_db)
):
    response = None
    try:
        response = binIssuers.create(session=db, data=data)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON create-binIssuers -- {err}',
            "data": {}
        }
    return {
        "error": False,
        "message": None,
        "data": binIssuersAddResponse.from_orm(response) or []
    }


@router.get(
    '/list_issuer',
    status_code=status.HTTP_200_OK
)
def list_issuer(
    db: Session = Depends(get_db)
):
    response = None
    try:
        response = binIssuers.list_all(session=db)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON list_all-binIssuers -- {err}',
            "data": {}
        }
    return {
        "error": False,
        "message": None,
        "data": binIssuersListAllResponse(data=response) or []
    }


@router.post(
    '/create_bin',
    status_code=status.HTTP_200_OK
)
def create_bin(
    data: binnerAdd,
    response: Response,
    db: Session = Depends(get_db)
):
    response = None
    try:
        response = binners.create(session=db, data=data)
    except InternalException as err_int:
        raise err_int
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON create-binners -- {err}',
            "data": {}
        }
    return {
        "error": False,
        "message": None,
        "data": binnerAddResponse.from_orm(response) or []
    }


@router.get(
    '/list_bin',
    status_code=status.HTTP_200_OK
)
def list_bin(
    db: Session = Depends(get_db)
):
    response = None
    try:
        response = binners.list_all(session=db)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON list_all-binners -- {err}',
            "data": {}
        }
    return {
        "error": False,
        "message": None,
        "data": binnerListAllResponse(data=response) or []
    }