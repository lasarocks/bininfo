


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



#from utils.binlookup import binlookup
from app.utils.cchelper import(
    formatar_cc,
    fmt_cc,
    luhn,
    gen_gg
)

from app.utils.utils import(
    add_arquivo,
    gibe_random_ua,
    b64decfixpad,
    load_json_file
)



import json

from app.utils.fakeUSAperson import FakePesonCheckoutAluvii



PATH_RESPONSE_CODES = 'app/files/oracle-response-codes.json'


status_response_codes = load_json_file(PATH_RESPONSE_CODES)


def get_status(status):
    temp = [x for x in status_response_codes if x.get('auth_auth_response', '') == status]
    if temp:
        return temp[0].get('auth_rmsg', '')
    return status_response_codes.get(status, '')






class oracleTryOut(reqPlus):
    def __init__(
        self,
        proxies={},
        timeout=(10,30)
    ):
        self.client_data = None
        super().__init__(proxies=proxies, timeout=timeout, default_useragent=gibe_random_ua())
    def check(self, cc_data):
        if self.initiate_session() != True:
            print(f'quebrou initiate_session --- {cc_data}')
            return False
        if self.initiate_cart() != True:
            print(f'quebrou initiate_cart --- {cc_data}')
            return False
        if self.send_pay() != True:
            print(f'quebrou send_pay --- {cc_data}')
            return False
        if self.send_session() != True:
            print(f'quebrou send_session --- {cc_data}')
            return False
        check_status = self.try_payment(cc_data)
        api_response = {
            'response_raw': None,
            'auth_response': -1,
            'response': None,
            'currency': 'BRL',
            'amount': '5.01'
        }
        if type(check_status) != dict:
            print(f'try_payment response != dict --- {type(check_status)} -- {check_status}')
        else:
            api_response.update(
                {
                    'response_raw': json.dumps(check_status)
                }
            )
            print(type(check_status))
            print(check_status)
            auth_response = check_status.get('auth_response', '')
            if auth_response:
                api_response.update({'auth_response': auth_response})
                response_status = get_status(status=auth_response)
                if response_status:
                    api_response.update(
                        {
                            'response': response_status,
                        }
                    )
        return api_response
    def gen_client(self):
        fake = FakePesonCheckoutAluvii()
        self.client_data = fake
    def parse_query_params(self, data):
        try:
            values = urllib.parse.urlencode(data)
        except Exception as err:
            print(f'oracleTryOut.parse_query_params exp --- {err}')
        else:
            return values
        return ''
    def initiate_session(self):
        self.new_session(ua=gibe_random_ua())
        self.gen_client()
        params_client = {
            'email': self.client_data.email
        }
        str_params_client = self.parse_query_params(data=params_client)
        url = f'https://signup-api.oraclecloud.com/20200828/payments?{str_params_client}'
        headers = self.gen_headers(
            referer='https://signup.oraclecloud.com/',
            origin='https://signup.oraclecloud.com',
            **{
                'Content-Type': 'application/json'
            }
        )
        payload = {
            "config": {
                "clientId": "OCI_ACCMGMT",
                "clientProfile": "CLOUD_SIGNUP",
                "country": "BR",
                "language": "en",
                "currency": "BRL",
                "organizationId": "378219",
                "paymentGateway": {
                    "merchantDefinedData": {
                        "skuList": "B88385",
                        "promoType": "Standard",
                        "campaignId": "",
                        "cloudAccountName": "wagnerleitedaniel",
                        "phoneCountryCode": "br",
                        "phoneNumber": "5519988653764"
                    }
                }
            },
            "items": [{
                "title": "Camada Grátis do Oracle Cloud"
            }],
            "address": {
                "line1": "Rua Moacyr Barbosa",
                "line2": "",
                "line3": "",
                "line4": "Jardim Campina Grande",
                "city": "Campinas",
                "postalCode": "13058-611",
                "state": "SP",
                "county": "",
                "province": "",
                "country": "BR",
                "emailAddress": "wagnerleitedani.el@gmail.com",
                "companyName": "",
                "firstName": "daniel",
                "lastName": "Wagner de Assis Leite"
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
            print(f'initiate_session exp --- {err}')
        else:
            if response.status_code == 201:
                token_payment = response.json().get('paymentToken', {})
                token_id = response.json().get('id', '')
                if token_payment and token_id:
                    response.set_status(value=True)
                    extra_data = {
                        'user': token_payment.get('userToken', ''),
                        'jwt': token_payment.get('jwtToken', ''),
                        'token_id': token_id
                    }
                    response.add_extra(extra_data)
                    return True
                else:
                    print(f'sem token_payment ou token_id')
            else:
                print(f'initiate session status code != 201 --- {response.status_code}')
        return False
    def initiate_cart(self):
        response_initiate_session = self.get_request('initiate_session', True)
        if not response_initiate_session:
            return False
        new_session_tokens = response_initiate_session.get_extra()
        id_cart = new_session_tokens.get('token_id', False)
        user_token = new_session_tokens.get('user', False)
        header_auth = new_session_tokens.get('jwt', False)
        if not id_cart or not user_token or not header_auth:
            return False
        url = f'https://shop.oracle.com/ords/osp/checkout/v1/headers/{id_cart}/secure-acceptance?lc=en&pt=card&tfa=signup.oraclecloud.com'
        headers = self.gen_headers(
            bearer=header_auth,
            **{
                'ps-token': user_token
            }
        )
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                method='GET'
            )
        except Exception as err:
            print(f'initiate_cart exp --- {err}')
        else:
            if response.status_code == 200:
                if self.client_data.email in response.text():
                    xbody = response.xtext()
                    if xbody:
                        xform = xbody.xpath('//form')
                        if xform:
                            xelemform = xform[0]
                            xelem_args_next = xelemform.xpath('./input')
                            if xelem_args_next:
                                url_next = xelemform.attrib.get('action', False)
                                payload_next = {}
                                for element in xelem_args_next:
                                    payload_next.update(
                                        {
                                            element.attrib.get('name', ''): element.attrib.get('value', '')
                                        }
                                    )
                                extra_data = {
                                    'url_action': url_next,
                                    'payload': payload_next
                                }
                                response.set_status(True)
                                response.add_extra(extra_data)
                                return True
                            else:
                                print(f'sem inputs')
                        else:
                            print(f'sem xform')
                    else:
                        print(f'sem xbody')
                else:
                    print(f'nao achou {self.client_data_email}')
            else:
                print(f'initiate cart status code != 200 -- {response.status_code}')
        return False
    def send_pay(self):
        response_initiate_cart = self.get_request('initiate_cart', True)
        if not response_initiate_cart:
            return False
        extra_data = response_initiate_cart.get_extra()
        url_use = extra_data.get('url_action', False)
        payload_use = extra_data.get('payload', False)
        if not url_use or not payload_use:
            return False
        url = url_use
        headers = self.gen_headers(
            referer='https://shop.oracle.com/',
            origin='https://shop.oracle.com',
            **{
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        payload = payload_use
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                data=payload,
                method='POST'
            )
        except Exception as err:
            print(f'send_pay exp --- {err}')
        else:
            if response.status_code == 200:
                if 'session_uuid' in response.text():
                    xbody = response.xtext()
                    if xbody:
                        xform = xbody.xpath('//form')
                        if xform:
                            xelemform = xform[0]
                            xsession_xpath = xelemform.xpath('./input[@name="session_uuid"]')
                            if xsession_xpath:
                                xsession = xsession_xpath[0].attrib.get('value', False)
                                url_next = xelemform.attrib.get('action', False)
                                if url_next and xsession:
                                    if not url_next.startswith('https://'):
                                        if not url_next.startswith('/'):
                                            url_next = f'/{url_next}'
                                        url_parse_sendpay = urllib.parse.urlparse(response.response.url)
                                        url_next = f'https://{url_parse_sendpay.hostname}{url_next}'
                                    extra_data = {
                                        'url_action': url_next,
                                        'session_id': xsession
                                    }
                                    response.set_status(True)
                                    response.add_extra(extra_data)
                                    return True
                                else:
                                    print(f'sem urlnext ou xsession')
                            else:
                                print(f'sem inputs')
                        else:
                            print(f'sem xform')
                    else:
                        print(f'sem xbody')
                else:
                    print(f'nao achou sessionuid')
            else:
                print(f'send_pay status code != 200 -- {response.status_code}')
        return False
    def send_session(self):
        response_send_pay = self.get_request('send_pay', True)
        if not response_send_pay:
            return False
        extra_data = response_send_pay.get_extra()
        url_use = extra_data.get('url_action', False)
        session_id = extra_data.get('session_id', False)
        if not url_use or not session_id:
            return False
        url = url_use
        headers = self.gen_headers(
            referer='https://secureacceptance.cybersource.com/embedded/pay',
            origin='https://secureacceptance.cybersource.com',
            **{
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        payload = {
            'session_uuid': session_id
        }
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                data=payload,
                method='POST'
            )
        except Exception as err:
            print(f'send_session exp --- {err}')
        else:
            if response.status_code == 200:
                xbody = response.xtext()
                if xbody:
                    xelem_authencity = xbody.xpath('//input[@name="authenticity_token"]')
                    if xelem_authencity:
                        autentico = xelem_authencity[0]
                        autentico_value = autentico.attrib.get('value', False)
                        if autentico_value:
                            response.set_status(True)
                            response.add_extra(
                                {
                                    'autentico': autentico_value,
                                    'session_id': session_id
                                }
                            )
                            return True
                        else:
                            print(f'sem autentico_value')
                    else:
                        print(f'sem xelem_authencity')
                else:
                    print(f'sem xbody')
            else:
                print(f'status code != 200 --- {response.status_code}')
        return False
    def try_payment(self, cc):
        response_send_session = self.get_request('send_session', True)
        if not response_send_session:
            return False
        extra_data = response_send_session.get_extra()
        cod_aut = extra_data.get('autentico', False)
        session_id = extra_data.get('session_id', False)
        cc_data = formatar_cc(cc)
        if not cod_aut or not session_id or not cc_data:
            return False
        url_session = response_send_session.response.url
        url_session = url_session[url_session.rindex('=')+1:].strip()
        #url = 'https://secureacceptance.cybersource.com/embedded?sessionid=722'
        url = f'https://secureacceptance.cybersource.com/embedded?sessionid={url_session}'
        headers = self.gen_headers(
            #referer='https://secureacceptance.cybersource.com/embedded/pay_load?sessionid=722',
            referer=response_send_session.response.url,
            origin='https://secureacceptance.cybersource.com',
            **{
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        cc_numero = cc_data.get('cc')
        card_type = '001' if cc_numero.startswith('4') else '002' if cc_numero[0] in ['5', '2'] else '003' if cc_numero.startswith('3') else '001'
        payload = {
            'utf8': '✓',
            'authenticity_token': cod_aut,
            'session_uuid': session_id,
            'bill_to_forename': 'daniel',
            'bill_to_surname': 'Wagner de Assis Leite',
            'bill_to_address_line1': 'Rua Moacyr Barbosa',
            'bill_to_address_line2': '',
            'bill_to_address_city': 'Campinas',
            'bill_to_address_state': 'SP',
            'bill_to_address_postal_code': '13058-611',
            'bill_to_phone': '5519988653764',
            'payment_method': 'card',
            'card_type': card_type,
            'card_number': cc_data.get('cc'),
            '__e.card_number': 'xKflOkemZpE05kRIphr27xLcTZ5KUTarJ+ADFFnzpuUU2tRipSPQwRnsfrDA8PWKQ4HWBHxaE/T/3f4ELlIAz/MrpNbudg53FYN7CdpSym2u6TTmoTIs4rsZWgdmTumDmOX7SqZDNaK9mZmqrPPZtJXQ7OPG20LhR1fe6aglmXR01S1LBWQJUfc8A2DV+vl1B2RPSe6uYaD1jX5ZiQBmByViNcG6JXkjT66U+GIclTQXouBw/RK8u3SPjMcaphh/9spFPDp994V7b01HgRZJKcHDCtMVlb/dpdMVEwFN14xzYXAzcJldkuppope+a2YxJxB+ffeMYAn65qoeUBZHXw==',
            'card_expiry_month': cc_data.get('month'),
            'card_expiry_year': f'20{cc_data.get("year")}',
            'card_cvn': cc_data.get('cvv'),
            '__e.card_cvn': 'bJ5olvsOccTlgw+nGYJTF9VZEWIgZ3NW9SRH86FwDi70DdIhNM5eqmKnAJo0mUBM6eAI8zmHPMd+kDEf4hgaQ7uKAJNSQ5If9VXigXnbuT7YB4Gvg5yhR/Y2ZWsWcjw4/5svlvcn8jHNaSTH03Bwj5OQ+BdSt9UsDNAC9KpbiHZIYyA8EjMPdIpoq8+4AJXR2k7Ok+7EvxdZ/UFl3qffDz+SehBJhaobcpWZIyli+T38sA/TEfaijuJi3H32Fa/M2a1xSUFWqzmAraxW9hv7TqZpwSG8juBNA5QKzljWvrIWygYhk5ejbMbNc2JQYBTw9PqQKXa83Oxca70YSioEGg==',
            'customer_utc_offset': '0',
        }
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                data=payload,
                method='POST'
            )
        except Exception as err:
            print(f'try_payment exp --- {err}')
        else:
            if response.status_code == 200:
                last_4 = cc_numero[len(cc_numero)-4:]
                if last_4 in response.text():
                    xbody = response.xtext()
                    if xbody:
                        keys_relevantes = [
                            'reason_code',
                            'auth_response',
                            'auth_avs_code',
                            'decision',
                            'message',
                            'auth_insights_response_category_code',
                        ]
                        valores_keys = {}
                        for key in keys_relevantes:
                            x_code_value = xbody.xpath(f'//input[@name="{key}"]')
                            if x_code_value:
                                xc = x_code_value[0]
                                valores_keys.update(
                                    {
                                        key: xc.attrib.get('value', False)
                                    }
                                )
                        return valores_keys
                        print(f'{cc_data} --- {valores_keys}')
                    else:
                        print(f'sem xbody')
                else:
                    print(f'nao achou 4 digitos --- {last_4}')
            else:
                print(f'try_payment status 200')
        return False

























