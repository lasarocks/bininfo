from app.core.reqPlus import reqPlus

from app.utils.exceptions import(
    expInvalidRequest,
    expInvalidRequestsResponse,
    invalidCredentials,
    userNotFound,
    captchaWrong,
    expMaxRetries,
    expSpecialTimeOut
)

import urllib

from app.utils.cchelper import(
    formatar_cc,
    fmt_cc,
    luhn,
    gen_gg
)

from app.utils.utils import(
    add_arquivo,
    gibe_random_ua,
    b64decfixpad
)



import json

from app.utils.fakeUSAperson import FakePesonCheckoutAluvii



class enduranceBinlookup(reqPlus):
    def __init__(
        self,
        proxies={},
        timeout=(10,30)
    ):
        self.client_data = None
        super().__init__(proxies=proxies, timeout=timeout, default_useragent=gibe_random_ua())
    def bin1(self, cc_raw):
        self.new_session(ua=gibe_random_ua())
        cc_data = formatar_cc(cc_raw)
        if not cc_data:
            print(f'invalid cc info ---- {cc_raw}')
            return False
        url = 'https://securepay.svcs.endurance.com/v1/payments/token'
        headers = self.gen_headers(
            **{
                'Content-Type': 'application/json'
            }
        )
        exp_card_year = cc_data.get("year")
        if len(exp_card_year) == 4:
            exp_card_year = exp_card_year[2:]
        payload = {
            "clientId": "400005",
            "method": "CREDITCARD",
            "type": "MULTI",
            "creditCard": {
                "cardHolderName": "meu n none",
                "cardNumber": cc_data.get('cc'),
                "cardSecureCode": cc_data.get('cvv'),
                "cardExpiration": f'{cc_data.get("month")}{exp_card_year}'
            }
        }
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                json=payload,
                method='POST'
            )
        except Exception as err:
            print(f'enduranceBinlookup.bin1 exp --- {err}')
        else:
            if response.status_code == 201:
                data_bin = response.json().get('binData', {})
                if data_bin:
                    return data_bin
                else:
                    print(f'no binData')
            else:
                print(f'enduranceBinlookup.bin1 status_code != 201 --- {response.status_code}')
        return False
    def bin2(self, cc_raw):
        self.new_session(ua=gibe_random_ua())
        cc_data = formatar_cc(cc_raw)
        if not cc_data:
            print(f'invalid cc info ---- {cc_raw}')
            return False
        url = 'https://securepay.svcs.endurance.com/v1/payments/token'
        headers = self.gen_headers(
            **{
                'Content-Type': 'application/json'
            }
        )
        exp_card_year = cc_data.get("year")
        if len(exp_card_year) == 4:
            exp_card_year = exp_card_year[2:]
        payload = {
            "clientId": "860001",
            "method": "CREDITCARD",
            "type": "MULTI",
            "creditCard": {
                "cardNumber": cc_data.get('cc'),
                "cardSecureCode": cc_data.get('cvv'),
                "cardExpiryMonth": cc_data.get("month"),
                "cardExpiryYear": exp_card_year
            }
        }
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                json=payload,
                method='POST'
            )
        except Exception as err:
            print(f'enduranceBinlookup.bin2 exp --- {err}')
        else:
            if response.status_code == 201:
                data_bin = response.json().get('binData', {})
                if data_bin:
                    return data_bin
                else:
                    print(f'no binData')
            else:
                print(f'enduranceBinlookup.bin2 status_code != 201 --- {response.status_code}')
        return False
    def check_bin(self, cc_raw):
        temp = self.bin2(cc_raw)
        if temp:
            api_response = {
                'card_bin': temp.get('number', None),
                'card_brand': temp.get('brand', None),
                'card_bank': temp.get('bank', None),
                'card_country': temp.get('country', None),
                'card_type': temp.get('type', None),
                'card_category': temp.get('level', None)
            }
            return api_response
        return False