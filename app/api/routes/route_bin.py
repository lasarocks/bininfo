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
    binProducts,
    binInformation
)

from app.models.schemas.sapi import(
    baseAPIResponse
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
    binProductAddResponse,
    binInformationAdd,
    binInformationAddResponse,
    binUnico,
    binUnicoResponse,
    binUnicoResponseData
)




from app.exceptions.general import(
    ItemNotFound,
    InternalException,
    InvalidParameters
)


import json






router = APIRouter()


@router.post(
    '/create_special',
    status_code=status.HTTP_200_OK
)
def create_special(
    data: binUnico,
    response: Response,
    db: Session = Depends(get_db)
):
    # return {
    #     "data": data
    # }
    try:
        response_issuer = binIssuers.create(session=db, data=data.issuer)
        if response_issuer:
            bin_data = binnerAdd(id_issuer=response_issuer.id, **data.bin_data.dict())
            response_bin = binners.create(session=db, data=bin_data)
            if response_bin:
                bin_information_data = binInformationAdd(id_bin=response_bin.id, **data.bin_information.dict())
                response_info = binInformation.create(session=db, data=bin_information_data)
                network_responses = []
                for network in data.card_network:
                    response_new_network = CardNetwork.create(session=db, data=network)
                    if response_new_network:
                        bin_new_network = binNetworkAdd(id_bin=response_bin.id, id_network=response_new_network.id)
                        response_new_bin_network = binNetworks.create(session=db, data=bin_new_network)
                        if response_new_bin_network:
                            network_responses.append(response_new_network)
                product_responses = []
                for product in data.card_product:
                    response_new_product = CardProduct.create(session=db, data=product)
                    if response_new_product:
                        bin_new_product = binProductAdd(id_bin=response_bin.id, id_product=response_new_product.id)
                        response_new_bin_product = binProducts.create(session=db, data=bin_new_product)
                        if response_new_bin_product:
                            product_responses.append(response_new_product)
                if response_info:
                    binunico_data = binUnicoResponseData(
                        issuer=binIssuersAddResponse.from_orm(response_issuer),
                        bin=binnerAdd.from_orm(response_bin),
                        cvc=binInformationAddResponse.from_orm(response_info),
                        network=CardNetworkListAllResponse(data=network_responses),
                        product=CardProductListAllResponse(data=product_responses)
                    )
                    binunico_response = binUnicoResponse(error=False, message=None, data=binunico_data)
                    return binunico_response
                    return {
                        "error": False,
                        "message": None,
                        "data": {
                            "issuer": binIssuersAddResponse.from_orm(response_issuer),
                            "bin": binnerAdd.from_orm(response_bin),
                            "cvc": binInformationAddResponse.from_orm(response_info),
                            "network": CardNetworkListAllResponse(data=network_responses),
                            "product": CardProductListAllResponse(data=product_responses)
                        }
                    }
            print(bin_data)
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
        "data": binIssuersAddResponse.from_orm(response_issuer) or []
    }



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



@router.post(
    '/set_cvc_information',
    status_code=status.HTTP_200_OK
)
def set_cvc_information(
    data: binInformationAdd,
    response: Response,
    db: Session = Depends(get_db)
):
    response = None
    try:
        response = binInformation.create(session=db, data=data)
    except InternalException as err_int:
        raise err_int
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON set_cvc_information -- {err}',
            "data": {}
        }
    return {
        "error": False,
        "message": None,
        "data": binInformationAddResponse.from_orm(response) or []
    }


@router.get(
    '/find_card_bin/{card_number}',
    status_code=status.HTTP_200_OK
)
def find_card_bin(
    card_number: str,
    response: Response,
    db: Session = Depends(get_db)
):
    try:
        response_query = binners.find_bin(session=db, card_number=card_number)
    except Exception as err:
        return {
            "error": True,
            "message": f'EXCEPTION ON find_card_bin -- {err}',
            "data": {}
        }
    else:
        if not response_query:
            response.status_code = status.HTTP_404_NOT_FOUND
    return {
        "error": False,
        "message": None,
        "data": binnerAddResponse.from_orm(response_query) if response_query else response_query
    }