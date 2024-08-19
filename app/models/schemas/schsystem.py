from datetime import date
from pydantic import Field
from datetime import datetime
from app.models.schemas.base import baseSchema

from typing import Optional, List
from uuid import UUID



from app.utils.cchelper import(
    luhn,
    fmt_cc,
    formatar_cc
)


# class CheckCC(baseSchema):
#     ccnum: str
#     ccmonth: str
#     ccyear: str
#     cvv: str
#     def raw(self):
#         return f'{self.ccnum}|{self.ccmonth}|{self.ccyear}|{self.cvv}'






# class CheckCCRAW(baseSchema):
#     ccraw: str





# class ccrowne(baseSchema):
#     ccraw: str
#     def raw(self):
#         return formatar_cc(self.ccraw)



class CardBinEnduranceAdd(baseSchema):
    card_bin: str
    card_brand: str
    card_type: str
    card_category: str
    card_country: str
    card_bank: str
    


class CardBinEnduranceAddResponse(CardBinEnduranceAdd):
    id: UUID
    date_created: datetime




class CardBinCheckoutAdd(baseSchema):
    card_bin: str
    card_brand: str
    card_type: str
    card_category: str
    card_country: str
    card_bank: str
    product_id: Optional[str] = None
    product_type: Optional[str] = None



class CardBinCheckoutAddResponse(CardBinCheckoutAdd):
    id: UUID
    date_created: datetime




class CardBinPaypal1Add(baseSchema):
    card_bin: str
    card_brand: str
    card_type: str
    card_country: Optional[str] = None
    card_bank: Optional[str] = None
    card_networks: Optional[str] = None
    product_types: Optional[str] = None
    status: Optional[str] = None




class CardBinPaypal1AddResponse(CardBinPaypal1Add):
    id: UUID
    date_created: datetime




class CardBinAdd(baseSchema):
    card_bin: Optional[str] = None
    card_bin_extra: Optional[str] = None
    card_brand: Optional[str] = None
    card_type: Optional[str] = None
    card_level: Optional[str] = None
    card_country: Optional[str] = None
    card_bank: Optional[str] = None



class CardBinAddResponse(CardBinAdd):
    id: UUID
    date_created: datetime




# class CardAdd(baseSchema):
#     card_bin: Optional[str] = None
#     card_number: str
#     card_exp_month: str
#     card_exp_year: str
#     card_cvv: str
#     last_status: Optional[str] = None
#     last_gateway_id: Optional[str] = None
#     source: Optional[str] = None
#     def raw(self):
#         return f'{self.card_number}|{self.card_exp_month}|{self.card_exp_year}|{self.card_cvv}'



# class CardAddResponse(CardAdd):
#     id: UUID
#     date_created: datetime



# class CardRAW(baseSchema):
#     ccraw: str
#     def parse(self):
#         cc_data = formatar_cc(self.ccraw)
#         if cc_data:
#             return CardAdd(**{
#                 'card_bin': cc_data.get('cc')[0:6],
#                 'card_number': cc_data.get('cc'),
#                 'card_exp_month': cc_data.get('month'),
#                 'card_exp_year': cc_data.get('year'),
#                 'card_cvv': cc_data.get('cvv'),
#             })
#         return False





class CardBinProcessoutAdd(baseSchema):
    card_bin: str
    card_brand: Optional[str] = None
    card_type: Optional[str] = None
    card_category: Optional[str] = None
    card_country: Optional[str] = None
    card_bank: Optional[str] = None
    card_coscheme: Optional[str] = None
    card_preferred_scheme: Optional[str] = None
    product_type: Optional[str] = None



class CardBinProcessoutAddResponse(CardBinProcessoutAdd):
    id: UUID
    date_created: datetime





# class GatewayAdd(baseSchema):
#     description: str
#     key: str
#     name: str
#     accepted_brands: Optional[str] = None
#     status: Optional[bool] = None




# class GatewayAddResponse(GatewayAdd):
#     id: UUID
#     date_created: datetime





# class TransactionBase(baseSchema):
#     amount: Optional[str] = None
#     currency: Optional[str] = None
#     status: Optional[str] = None
#     response: Optional[str] = None
#     response_raw: Optional[str] = None



# class TransactionAdd(TransactionBase):
#     id_gateway: str
#     id_card: str


# class TransactionCreate(baseSchema):
#     id_gateway: str
#     id_card: str
#     def add(self):
#         return TransactionAdd(**{'id_gateway': self.id_gateway,'id_card': self.id_card})




# class TransactionAddResponse(TransactionBase):
#     id: UUID
#     id_gateway: UUID
#     id_card: UUID
#     date_created: datetime


# class TransactionRT(TransactionAddResponse):
#     Gateways: GatewayAddResponse


# class TransactionsResponse(baseSchema):
#     data: List[TransactionRT]




# class TransactionRT2(TransactionAddResponse):
#     Gateways: GatewayAddResponse
#     cards: CardAddResponse


# class TransactionsResponse2(baseSchema):
#     data: List[TransactionRT2]

