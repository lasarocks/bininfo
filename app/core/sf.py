
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


class saferpay(reqPlus):
    def __init__(
        self,
        proxies={},
        timeout=(10,30)
    ):
        self.client_data = None
        self.client_mail = 'juliettedrunk@fthcapital.com'
        super().__init__(proxies=proxies, timeout=timeout, default_useragent=gibe_random_ua())
    def initiate_session(self):
        self.new_session(ua=gibe_random_ua())
        url = f'https://test.saferpay.com/Fields/Api/242225/Initialize'
        headers = self.gen_headers(
            referer='https://shop.saferpay.eu/',
            origin='https://shop.saferpay.eu',
            **{
                'Content-Type': 'application/json; charset=UTF-8',
                'Saferpay-AuthToken': '8ce79709-3546-4315-a5e9-e54823126574',
                'Saferpay-LibVersion': '1.8.0',
                'Saferpay-Url': 'https://shop.saferpay.eu/saferpayintegration/HostedFields.php'
            }
        )
        payload = {}
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                json=payload,
                method='POST'
            )
        except Exception as err:
            print(f'initiate_session exp --- {err}')
        else:
            if response.status_code == 200:
                token = response.json().get('token', False)
                if token:
                    response.set_status(True)
                    response.add_extra(
                        {
                            'token': token
                        }
                    )
                    return True
                else:
                    print(f'sem token')
            else:
                print(f'status_code != 200 --- {response.status_code}')
        return False
    def check_card(self, ccn):
        response_initiate_session = self.get_request('initiate_session', True)
        if not response_initiate_session:
            print(f'no response_initiate_session')
            return False
        token = response_initiate_session.get_extra().get('token', False)
        if not token:
            print(f'no token')
            return False
        url = f'https://test.saferpay.com/Fields/Api/242225/CheckCard/{token}'
        headers = self.gen_headers(
            **{
                'Content-Type': 'application/json',
            }
        )
        payload = {
            'cardnumber': ccn
        }
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                json=payload,
                method='POST'
            )
        except Exception as err:
            print(f'check_card exp --- {err}')
        else:
            if response.status_code == 200:
                hs1 = 'isCvcMandatory'
                if hs1 in response.text():
                    response.set_status(True)
                    response.add_extra(response.json())
                    return True
                else:
                    print(f'nao achou {hs1}')
            else:
                print(f'status_code != 200 --- {response.status_code}')
        return False
    def check(self, cc_raw):
        cc_data = formatar_cc(cc_raw)
        if not cc_data:
            print(f'no cc_data')
            return False
        if not self.get_request('initiate_session', True):
            if not self.initiate_session() == True:
                print(f'initiate_session failed ---')
                return False
        if self.check_card(ccn=cc_data.get('cc')) == True:
            return self.get_request('check_card', True).get_extra()
        return False

