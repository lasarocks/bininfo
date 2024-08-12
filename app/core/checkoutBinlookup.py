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


class checkoutBinlookup(reqPlus):
    def __init__(
        self,
        proxies={},
        timeout=(10,30)
    ):
        self.client_data = None
        self.client_mail = 'juliettedrunk@fthcapital.com'
        super().__init__(proxies=proxies, timeout=timeout, default_useragent=gibe_random_ua())
    def gen_client(self):
        fake = FakePesonCheckoutAluvii()
        self.client_data = fake
    def check_bin(self, cc_raw):
        self.new_session(ua=gibe_random_ua())
        self.gen_client()
        cc_data = formatar_cc(cc_raw)
        if not cc_data:
            print(f'invalid cc info ---- {cc_raw}')
            return False
        url = 'https://api.checkout.com/tokens'
        headers = self.gen_headers(
            referer='https://js.checkout.com/',
            origin='https://js.checkout.com',
            **{
                'Authorization': 'pk_tt5pcq7gh7fg3xcsizsbf25v7m5',
                'Content-Type': 'application/json',
            }
        )
        payload = {
            'type': 'card',
            'number': cc_data.get("cc"),
            'expiry_month': cc_data.get("month"),
            'expiry_year': cc_data.get("year"),
            'cvv': cc_data.get("cvv"),
            'name': 'luis m carlos',
            'phone': {},
            'preferred_scheme': '',
            'requestSource': 'JS',
        }
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                json=payload,
                method='POST'
            )
        except Exception as err:
            print(f'check_bin exp --- {err}')
        else:
            if response.status_code == 201:
                look_keys = ['scheme', 'bin', 'card_type', 'card_category', 'issuer', 'issuer_country', 'product_id', 'product_type', 'phone']
                data_response = {}
                for key in look_keys:
                    data_response.update(
                        {
                            key: response.json().get(key, None)
                        }
                    )
                if data_response:
                    api_response = {
                        'card_bin': data_response.get('bin', None),
                        'card_brand': data_response.get('scheme', None),
                        'card_type': data_response.get('card_type', None),
                        'card_category': data_response.get('card_category', None),
                        'card_country': data_response.get('issuer_country', None),
                        'card_bank': data_response.get('issuer', None),
                        'product_id': data_response.get('product_id', None),
                        'product_type': data_response.get('product_type', None),
                    }
                    response.set_status(True)
                    response.add_extra(
                        {
                            'response': data_response,
                            'api_response': api_response
                        }
                    )
                    return True
                else:
                    print(f'no data_response')
            else:
                print(f'checkoutBinlookup.initiate_session status_code != 201 -- {response.status_code}')
        return False