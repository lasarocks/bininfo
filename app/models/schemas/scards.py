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



class CardAdd(baseSchema):
    card_bin: Optional[str] = None
    card_number: str
    card_exp_month: str
    card_exp_year: str
    card_cvv: str
    last_status: Optional[str] = None
    last_gateway_id: Optional[str] = None
    source: Optional[str] = None
    def raw(self):
        return f'{self.card_number}|{self.card_exp_month}|{self.card_exp_year}|{self.card_cvv}'



class CardAddResponse(CardAdd):
    id: UUID
    date_created: datetime



class CardRAW(baseSchema):
    ccraw: str
    def parse(self):
        cc_data = formatar_cc(self.ccraw)
        if cc_data:
            return CardAdd(**{
                'card_bin': cc_data.get('cc')[0:6],
                'card_number': cc_data.get('cc'),
                'card_exp_month': cc_data.get('month'),
                'card_exp_year': cc_data.get('year'),
                'card_cvv': cc_data.get('cvv'),
            })
        return False


class CardsListAllResponse(baseSchema):
    data: List[CardAddResponse]