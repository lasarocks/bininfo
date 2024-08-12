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


class processoutBinlookup(reqPlus):
    def __init__(
        self,
        proxies={},
        timeout=(10,30)
    ):
        self.client_data = None
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
        url = 'https://api.processout.com/cards'
        headers = self.gen_headers(
            referer='https://js.processout.com/',
            origin='https://js.processout.com',
            **{
                'Authorization': 'Basic cHJval9Lak0yR25vbGVpc2RVZ3R5UE1qY0R1ZGVpczFUQlNEUDo=',
                'Content-Type': 'application/json',
                'API-Version': '1.3.0.0',
            }
        )
        payload = {
            'name': self.client_data.full_name,
            'contact': {},
            'device': {
                'request_origin': 'web',
                'app_color_depth': 24,
                'app_language': 'en-US',
                'app_screen_height': 1080,
                'app_screen_width': 1920,
                'app_timezone_offset': 0,
                'app_java_enabled': False,
            },
            'request_origin': 'web',
            'app_color_depth': 24,
            'app_language': 'en-US',
            'app_screen_height': 1080,
            'app_screen_width': 1920,
            'app_timezone_offset': 0,
            'app_java_enabled': False,
            'number': cc_data.get("cc"),
            'exp_month': cc_data.get("month"),
            'exp_year': cc_data.get("year"),
            'cvc2': cc_data.get("cvv"),
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
            if response.status_code == 200:
                if response.json().get('success', False) == True:
                    data_bin_card = response.json().get('card', {})
                    if data_bin_card:
                        look_keys = ['scheme', 'type', 'bank_name', 'brand', 'category', 'iin', 'country_code', 'co_scheme', 'preferred_scheme']
                        data_response = {}
                        for key in look_keys:
                            data_response.update(
                                {
                                    key: data_bin_card.get(key, None)
                                }
                            )
                        if data_response:
                            api_response = {
                                'card_bin': data_response.get('iin', None),
                                'card_brand': data_response.get('scheme', None),
                                'card_type': data_response.get('type', None),
                                'card_category': data_response.get('category', None),
                                'card_country': data_response.get('country_code', None),
                                'card_bank': data_response.get('bank_name', None),
                                'card_coscheme': data_response.get('co_scheme', None),
                                'card_preferred_scheme': data_response.get('preferred_scheme', None),
                                'product_type': data_response.get('brand', None),
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
                        print('no data_bin_card --- response.json().get(card) returned {}')
                else:
                    print(f'success != True')
            else:
                print(f'processoutBinlookup.initiate_session status_code != 200 -- {response.status_code}')
        return False