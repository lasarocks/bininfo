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




class stripeVBVExternalWhatbox(reqPlus):
    def __init__(
        self,
        username,
        password,
        proxies={},
        timeout=(10,30)
    ):
        self.client_data = None
        self.username = username
        self.password = password
        super().__init__(proxies=proxies, timeout=timeout, default_useragent=gibe_random_ua())
    def url_garimpa(self, url):
        try:
            url_query_parsed = urllib.parse.parse_qsl(urllib.parse.urlparse(url).query)
        except Exception as err:
            print(f'url_garimpa exp --- {url} --- {err}')
        else:
            if url_query_parsed:
                query = {}
                for item in url_query_parsed:
                    query.update(
                        {
                            item[0]: item[1]
                        }
                    )
                return query
        return {}
    def initiate_session(self):
        self.new_session(ua=gibe_random_ua())
        url = f'https://whatbox.ca/login'
        headers = self.gen_headers()
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                method='GET'
            )
        except Exception as err:
            print(f'initiate_session exp --- {err}')
        else:
            if response.status_code == 200:
                hs1 = 'csrf_token_ip'
                if hs1 in response.text():
                    xbody = response.xtext()
                    xelem = xbody.xpath(f'//input[@name="{hs1}"]')
                    if xelem:
                        elem = xelem[0]
                        csrf = elem.attrib.get('value', False)
                        if csrf:
                            response.set_status(True)
                            response.add_extra(
                                {
                                    'csrf': csrf
                                }
                            )
                            return True
                        else:
                            print(f'nao achou value do csrf')
                    else:
                        print(f'nao achou xelem')
                else:
                    print(f'nao achou {hs1} no text')
            else:
                print(f'status_code initiate_session != 200 -- {response.status_code}')
        return False
    def login(self):
        response_session = self.get_request('initiate_session', True)
        if not response_session:
            return False
        extra_data = response_session.get_extra()
        csrf_token = extra_data.get('csrf', None)
        if not csrf_token:
            return False
        url = f'https://whatbox.ca/login'
        headers = self.gen_headers(
            **{
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        payload = {
            'csrf_token_ip': csrf_token,
            'username': self.username,
            'password': self.password
        }
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                data=payload,
                method='POST'
            )
        except Exception as err:
            print(f'login exp --- {err}')
        else:
            if response.status_code in (301,302,303):
                redirect_res = response.headers.get('location', '')
                if redirect_res == '/news':
                    response.set_status(True)
                    return True
                else:
                    print(f'ganho redirect outro lugar ---- {redirect_res} ---')
            else:
                print(f'login status code not int 301 302 303 --- {response.status_code}')
        return False
    def create_invoice(self):
        response_login = self.get_request('login', True)
        if not response_login:
            return False
        url = 'https://whatbox.ca/pay/new?plan=NEW-1800G&currency=USD&country=US&payment=Stripe'
        headers = self.gen_headers()
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                method='GET'
            )
        except Exception as err:
            print(f'create_invoice exp --- {err}')
        else:
            if response.status_code == 200:
                hs1 = 'data-stripe'
                if hs1 in response.text():
                    xbody = response.xtext()
                    xelem = xbody.xpath('//div[@id="data-stripe"]')
                    if xelem:
                        can_continue = True
                        elem = xelem[0]
                        keys_stripe_looking = {
                            'data-publishable-key': None,
                            'data-client-secret': None
                        }
                        for key in keys_stripe_looking:
                            temp = elem.attrib.get(key, False)
                            if not temp:
                                print(f'create_invoice didnt find stripe key --- {key}')
                                can_continue = False
                            else:
                                keys_stripe_looking.update({key: temp})
                        if can_continue is True:
                            response.set_status(True)
                            response.add_extra(
                                keys_stripe_looking
                            )
                            return True
                        else:
                            print(f'can_continue is not True')
                    else:
                        print(f'didnt find xelem')
                else:
                    print(f'didnt find hs1 {hs1} on text')
            else:
                print(f'create_invoice status_code != 200 --- {response.status_code}')
        return False
    def add_payment(self, cc_raw):
        response_invoice = self.get_request('create_invoice', True)
        if not response_invoice:
            return False
        extra_data = response_invoice.get_extra()
        stp_pk_key = extra_data.get('data-publishable-key', False)
        stp_secret = extra_data.get('data-client-secret', False)
        cc_data = formatar_cc(cc_raw)
        if not stp_pk_key or not stp_secret or not cc_data:
            return False
        stp_intent = stp_secret[0:stp_secret.index('_secret')]
        url = f'https://api.stripe.com/v1/payment_intents/{stp_intent}/confirm'
        headers = self.gen_headers(
            referer='https://js.stripe.com/',
            origin='https://js.stripe.com',
            **{
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        payload = {
            "return_url": "https://resellerspalace.bigcartel.com/checkout/YX4RO8FHNSTZE26A3VPK3Q5UJ?checkout_polling_url=https%3A%2F%2Fresellerspalace.bigcartel.com%2Fcheckout%2FYX4RO8FHNSTZE26A3VPK3Q5UJ&stripe_payment_type=link",
            "setup_future_usage": "off_session",
            "payment_method_data[type]": "card",
            "payment_method_data[card][number]": cc_data.get('cc'),
            "payment_method_data[card][cvc]": cc_data.get('cvv'),
            "payment_method_data[card][exp_month]": cc_data.get('month'),
            "payment_method_data[card][exp_year]": cc_data.get('year'),
            "payment_method_data[guid]": "3b08016f-ef72-4686-b1b0-8219622144e29a5ed0",
            "payment_method_data[muid]": "62dab90b-b1c8-46ac-b97f-717a8653dbe383316c",
            "payment_method_data[sid]": "17c88c54-c33c-44f0-a9d0-84225940e4897c434c",
            "payment_method_data[pasted_fields]": "number",
            "payment_method_data[payment_user_agent]": "stripe.js/6c8b4b9154; stripe-js-v3/6c8b4b9154; card-element",
            "payment_method_data[referrer]": "https://whatbox.ca",
            "payment_method_data[time_on_page]": "137323",
            "expected_payment_method_type": "card",
            "use_stripe_sdk": "false",
            "key": stp_pk_key,
            "client_secret": stp_secret
        }
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                data=payload,
                method='POST'
            )
        except Exception as err:
            print(f'add_payment exp --- {err}')
        else:
            if response.status_code == 200:
                next_action = response.json().get('next_action', {})
                if next_action:
                    next_action_type = next_action.get('type', False)
                    if next_action_type:
                        if next_action_type == 'use_stripe_sdk' or next_action_type == 'redirect_to_url':
                            stp_paysrc = None
                            if next_action_type == 'use_stripe_sdk':
                                stp_paysrc = next_action.get('use_stripe_sdk', {}).get('three_d_secure_2_source', None)
                            else:
                                url_next = next_action.get('redirect_to_url', {}).get('url', None)
                                if url_next:
                                    stp_paysrc = self.url_garimpa(url_next).get('source', None)
                            if stp_paysrc:
                                response.set_status(True)
                                response.add_extra(
                                    {
                                        'paysrc': stp_paysrc,
                                        'pkkey': stp_pk_key
                                    }
                                )
                                return True
                            else:
                                print(f'no stp_paysrc')
                        else:
                            print(f'next_action_type != "use_stripe_sdk" --- {next_action_type}')
                    else:
                        print(f'nao achou next_action_type')
                else:
                    print(f'nao achou next_action')
            elif response.status_code == 400:
                error_msg = response.json().get('error', {}).get('code', '')
                if error_msg == 'payment_intent_unexpected_state':
                    print(f'payment intent error msg == payment_intent_unexpected_state')
                    return 'REDO'
                else:
                    print(f'response. status_code == 400, error code == {error_msg}')
            elif response.status_code == 402:
                print(f'402 VBV----')
                error_msg = response.json().get('error', {}).get('code', '')
                if error_msg:
                    response.add_extra(
                        {
                            'state': 'failed_lookup',
                            'ares': None,
                            'code': error_msg
                        }
                    )
                    print(f'402 VBV---- ERROR_CODE === {error_msg}')
                    return {'code': error_msg}
                print(response.json())
            else:
                print(f'status_code != 200 --- {response.status_code}')
        return False
    def auth_vbv(self):
        response_add_payment = self.get_request('add_payment', True)
        if not response_add_payment:
            return False
        extra_data = response_add_payment.get_extra()
        stp_paysrc = extra_data.get('paysrc', False)
        stp_pk_key = extra_data.get('pkkey', False)
        if not stp_paysrc or not stp_pk_key:
            return False
        url = f'https://api.stripe.com/v1/3ds2/authenticate'
        headers = self.gen_headers(
            referer='https://js.stripe.com/',
            origin='https://js.stripe.com',
            **{
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        payload = {
            "source": stp_paysrc,
            "browser": "{\"fingerprintAttempted\":true,\"fingerprintData\":null,\"challengeWindowSize\":null,\"threeDSCompInd\":\"Y\",\"browserJavaEnabled\":false,\"browserJavascriptEnabled\":true,\"browserLanguage\":\"en-US\",\"browserColorDepth\":\"24\",\"browserScreenHeight\":\"1080\",\"browserScreenWidth\":\"1920\",\"browserTZ\":\"0\",\"browserUserAgent\":\"Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0\"}",
            "one_click_authn_device_support[hosted]": "false",
            "one_click_authn_device_support[same_origin_frame]": "false",
            "one_click_authn_device_support[spc_eligible]": "false",
            "one_click_authn_device_support[webauthn_eligible]": "false",
            "one_click_authn_device_support[publickey_credentials_get_allowed]": "false",
            "key": stp_pk_key
        }
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                data=payload,
                method='POST'
            )
        except Exception as err:
            print(f'auth_vbv exp --- {err}')
        else:
            if response.status_code == 200:
                response.set_status(True)
                state = response.json().get('state', False)
                ares = response.json().get('ares', {})
                extra = {
                    'state': state
                }
                if ares:
                    extra.update(
                        {
                            'ares': ares
                        }
                    )
                response.add_extra(extra)
                return True
            else:
                print(f'auth_vbv status_code != 200 --- {response.status_code}')
        return False
    def check_inside_creq(self):
        response_auth_vbv = self.get_request('auth_vbv', True)
        if not response_auth_vbv:
            return False
        url_acl = response_auth_vbv.json().get('ares', {}).get('acsURL', False)
        creq_acl = response_auth_vbv.json().get('creq', None)
        if not url_acl or not creq_acl:
            print(f'no url_acl or creq_acl')
            return False
        headers = self.gen_headers(
            referer='https://js.stripe.com/',
            origin='https://js.stripe.com',
            **{
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        payload = {
            'creq': creq_acl
        }
        card_status = None
        try:
            response = self._make_call(
                url=url_acl,
                headers=headers,
                data=payload,
                method='POST'
            )
        except Exception as err:
            print(f'check_inside_creq exp --- {err}')
        else:
            if response.status_code == 200:
                xbody = response.xtext()
                if xbody:
                    xelem_error = xbody.xpath('//*[@id="errorMessage"]')
                    xelem_actions = xbody.xpath('//div[@id="formactions"]')
                    if xelem_error:
                        xelem_error = xelem_error[0]
                        msg_error = xelem_error.text_content().strip()
                        if msg_error:
                            card_status = msg_error.strip()
                    if card_status is None:
                        if xelem_actions:
                            xelem_actions = xelem_actions[0]
                            elem_action = (xelem_actions.xpath('./a[@data-action="resend"]') or [None])[0]
                            if elem_action:
                                card_status = elem_action.text_content().strip()
                if not card_status:
                    hs1 = 'WHATBOX INC'
                    if hs1 in response.text():
                        card_status = 'OK'
                if card_status:
                    response.set_status(True)
                    response.add_extra(
                        {
                            'card_status': card_status
                        }
                    )
            else:
                print(f'response check_inside_creq != 200')
            return response
        return False
    def vbv(self, cc_raw):
        if not self.get_request('initiate_session', True):
            if not self.initiate_session() == True:
                print(f'initiate_session failed')
                return False
        if not self.get_request('login', True):
            if not self.login() == True:
                print(f'login failed')
                return False
        if not self.get_request('create_invoice', True):
            if not self.create_invoice() == True:
                print(f'create_invoice failed')
                return False
        response_add_payment = self.add_payment(cc_raw=cc_raw)
        if not response_add_payment == True:
            if not response_add_payment:
                print(f'add_payment {cc_raw} failed')
                return False
            else:
                if response_add_payment == 'REDO':
                    print(f'redo requested --- {cc_raw}')
                    self._requests = {}
                    return self.vbv(cc_raw=cc_raw)
                elif type(response_add_payment) == dict:
                    return self.get_request('add_payment')
        if not self.auth_vbv() == True:
            print(f'auth_vbv failed !!')
            return False
        return self.get_request('auth_vbv')
    def cvbv(self, cc_raw):
        return self.vbv(cc_raw=cc_raw)







def newvbv():
    u = 'pedromathias77mg'
    s = '123456'
    return stripeVBVExternalWhatbox(username=u, password=s)