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
    binners,
    CardNetwork,
    binNetworks,
    CardProduct,
    binProducts
)



from app.models.schemas.sbinna import(
    binIssuersAdd,
    binIssuersAddResponse,
    binnerAdd,
    binnerAddResponse,
    binIssuersListAllResponse,
    binnerListAllResponse,
    CardNetworkAdd,
    CardNetworkAddResponse,
    CardNetworkListAllResponse,
    binNetworkAdd,
    binNetworkAddResponse,
    CardProductAdd,
    CardProductAddResponse,
    CardProductListAllResponse,
    binProductAdd,
    binProductAddResponse
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
    except InternalException as err_int:
        raise err_int
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


@router.post(
    '/create_network',
    status_code=status.HTTP_200_OK
)
def create_network(
    data: CardNetworkAdd,
    response: Response,
    db: Session = Depends(get_db)
):
    response = None
    try:
        response = CardNetwork.create(session=db, data=data)
    except InternalException as err_int:
        raise err_int
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON create-network -- {err}',
            "data": {}
        }
    return {
        "error": False,
        "message": None,
        "data": CardNetworkAddResponse.from_orm(response) or []
    }


@router.get(
    '/list_network',
    status_code=status.HTTP_200_OK
)
def list_network(
    db: Session = Depends(get_db)
):
    response = None
    try:
        response = CardNetwork.list_all(session=db)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON list_all-CardNetwork -- {err}',
            "data": {}
        }
    return {
        "error": False,
        "message": None,
        "data": CardNetworkListAllResponse(data=response) or []
    }


@router.post(
    '/create_bin_network',
    status_code=status.HTTP_200_OK
)
def create_bin_network(
    data: binNetworkAdd,
    response: Response,
    db: Session = Depends(get_db)
):
    response = None
    try:
        response = binNetworks.create(session=db, data=data)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON create-binNetworks -- {err}',
            "data": {}
        }
    return {
        "error": False,
        "message": None,
        "data": binNetworkAddResponse.from_orm(response) or []
    }



@router.post(
    '/create_product',
    status_code=status.HTTP_200_OK
)
def create_product(
    data: CardProductAdd,
    response: Response,
    db: Session = Depends(get_db)
):
    response = None
    try:
        response = CardProduct.create(session=db, data=data)
    except InternalException as err_int:
        raise err_int
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON create-product -- {err}',
            "data": {}
        }
    return {
        "error": False,
        "message": None,
        "data": CardProductAddResponse.from_orm(response) or []
    }


@router.get(
    '/list_product',
    status_code=status.HTTP_200_OK
)
def list_product(
    db: Session = Depends(get_db)
):
    response = None
    try:
        response = CardProduct.list_all(session=db)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON list_all-CardProduct -- {err}',
            "data": {}
        }
    return {
        "error": False,
        "message": None,
        "data": CardProductListAllResponse(data=response) or []
    }


@router.post(
    '/create_bin_product',
    status_code=status.HTTP_200_OK
)
def create_bin_product(
    data: binProductAdd,
    response: Response,
    db: Session = Depends(get_db)
):
    response = None
    try:
        response = binProducts.create(session=db, data=data)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON create-binProducts -- {err}',
            "data": {}
        }
    return {
        "error": False,
        "message": None,
        "data": binProductAddResponse.from_orm(response) or []
    }