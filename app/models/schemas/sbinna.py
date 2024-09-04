from pydantic import Field
from datetime import datetime
from app.models.schemas.base import baseSchema

from typing import Optional, List, Dict
from uuid import UUID

from app.models.schemas.sapi import(
    baseAPIResponse
)



class binIssuersAdd(baseSchema):
    country: Optional[str] = None
    name: Optional[str] = None
    name_alternative: Optional[str] = None
    






class binIssuersAddResponse(binIssuersAdd):
    id: int
    date_created: datetime


class binIssuersListAllResponse(baseSchema):
    data: List[binIssuersAddResponse]



class binnerBase(baseSchema):
    card_bin: str
    card_type: Optional[str] = None
    card_category: Optional[str] = None
    product_category: Optional[str] = None
    cvc_mandatory: Optional[bool] = None


class binnerAdd(binnerBase):
    id_issuer: int



class binInformationBase(baseSchema):
    has_cvc: Optional[bool] = None
    cvc_mandatory: Optional[bool] = None


class binInformationAdd(binInformationBase):
    id_bin: int








class binInformationAddResponse(binInformationAdd):
    id: int
    date_created: datetime



class CardNetworkAdd(baseSchema):
    name: str
    description: Optional[str] = None





class CardNetworkAddResponse(CardNetworkAdd):
    id: int
    date_created: datetime


class CardNetworkListAllResponse(baseSchema):
    data: List[CardNetworkAddResponse]




class CardProductAdd(baseSchema):
    name: str
    description: Optional[str] = None


class CardProductAddResponse(CardProductAdd):
    id: int
    date_created: datetime


class CardProductListAllResponse(baseSchema):
    data: List[CardProductAddResponse]





class binNetworkAdd(baseSchema):
    id_bin: int
    id_network: int


class binNetworkAddResponse(binNetworkAdd):
    id: int
    date_created: datetime
    networks: CardNetworkAddResponse



class binProductAdd(baseSchema):
    id_bin: int
    id_product: int


class binProductAddResponse(binProductAdd):
    id: int
    date_created: datetime
    products: CardProductAddResponse





class binnerAddResponse(binnerAdd):
    id: int
    date_created: datetime
    binIssuers: binIssuersAddResponse
    bin_networks: List[binNetworkAddResponse]
    products: List[binProductAddResponse]
    bin_information: List[binInformationAddResponse]


class binnerListAllResponse(baseSchema):
    data: List[binnerAddResponse]


class binUnico(baseSchema):
    issuer: binIssuersAdd
    bin_data: binnerBase
    bin_information: binInformationBase
    card_network: List[CardNetworkAdd]
    card_product: List[CardProductAdd]



class binUnicoResponseData(baseSchema):
    issuer: binIssuersAddResponse
    bin: binnerAdd
    cvc: binInformationAddResponse
    network: CardNetworkListAllResponse
    product: CardProductListAllResponse


class binUnicoResponse(baseAPIResponse):
    data: binUnicoResponseData
