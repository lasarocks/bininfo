from pydantic import Field
from datetime import datetime
from app.models.schemas.base import baseSchema

from typing import Optional, List
from uuid import UUID




class binIssuersAdd(baseSchema):
    country: Optional[str] = None
    name: Optional[str] = None
    name_alternative: Optional[str] = None
    



class binIssuersAddResponse(binIssuersAdd):
    #id: UUID
    id: int
    date_created: datetime


class binIssuersListAllResponse(baseSchema):
    data: List[binIssuersAddResponse]



class binnerAdd(baseSchema):
    #id_issuer: str
    id_issuer: int
    card_bin: str
    card_type: Optional[str] = None
    card_category: Optional[str] = None
    product_category: Optional[str] = None
    cvc_mandatory: Optional[bool] = None





class CardNetworkAdd(baseSchema):
    name: str
    description: Optional[str] = None


class CardNetworkAddResponse(CardNetworkAdd):
    #id: UUID
    id: int
    date_created: datetime


class CardNetworkListAllResponse(baseSchema):
    data: List[CardNetworkAddResponse]




class CardProductAdd(baseSchema):
    name: str
    description: Optional[str] = None


class CardProductAddResponse(CardProductAdd):
    #id: UUID
    id: int
    date_created: datetime


class CardProductListAllResponse(baseSchema):
    data: List[CardProductAddResponse]





class binNetworkAdd(baseSchema):
    #id_bin: str
    id_bin: int
    #id_network: str
    id_network: int


class binNetworkAddResponse(binNetworkAdd):
    #id: UUID
    id: int
    date_created: datetime
    networks: CardNetworkAddResponse



class binProductAdd(baseSchema):
    #id_bin: str
    id_bin: int
    #id_product: str
    id_product: int


class binProductAddResponse(binProductAdd):
    #id: UUID
    id: int
    date_created: datetime
    products: CardProductAddResponse





class binnerAddResponse(binnerAdd):
    #id: UUID
    id: int
    date_created: datetime
    binIssuers: binIssuersAddResponse
    bin_networks: List[binNetworkAddResponse]
    products: List[binProductAddResponse]


class binnerListAllResponse(baseSchema):
    data: List[binnerAddResponse]