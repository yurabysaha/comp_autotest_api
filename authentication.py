import json
import requests
import unittest
from baseSettings import *
import time

from authorization import test_authorization


class Test_001_ServerRegister(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_001_ServerRegister, self).__init__(*a, **kw)
        self.command_signup = 'auth/signup'
        self.url_signup = '{}/{}'.format(HOST, self.command_signup)
        self.s = requests.Session()

    def test_01_register_successfully(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        email_value = time.strftime("%d%m%Y" + "%H%M%S") + "@" + "test.com"
        userdata = json.dumps({"email": email_value, "full_name": "FullName"})
        response = self.s.post(self.url_signup, data=userdata, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)

    def test_02_register_empty_values(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        userdata = json.dumps({"email": "", "full_name": ""})
        response = self.s.post(self.url_signup, data=userdata, headers=headers)

        self.assertEqual(response.status_code, BADDATA)

    def test_03_register_wrong_email_format(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        userdata = json.dumps({"email": "test", "full_name": "test"})
        response = self.s.post(self.url_signup, data=userdata, headers=headers)

        self.assertEqual(response.status_code, BADDATA)

    def test_04_register_already_registered_email(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        userdata = json.dumps({"email": EMAIL, "full_name": "test"})
        response = self.s.post(self.url_signup, data=userdata, headers=headers)

        self.assertEqual(response.status_code, BADDATA)


class Test_002_ServerLogin(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_002_ServerLogin, self).__init__(*a, **kw)
        self.command_signin = 'auth/signin'
        self.url_signin = '{}/{}'.format(HOST, self.command_signin)
        self.s = requests.Session()

    def test_01_signed_in_successfully(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        userdata = json.dumps({ "email": EMAIL, "password": PSW})
        response = self.s.post(self.url_signin, data=userdata, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)


class Test_003_ServerLoginByFacebook(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_003_ServerLoginByFacebook, self).__init__(*a, **kw)
        self.command_signinbyfb = 'auth/signin/fb'
        self.url_signinbyfb = '{}/{}'.format(HOST, self.command_signinbyfb)
        self.s = requests.Session()

    def test_01_register_successfully(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        userdata = json.dumps({"access_token": FACEBOOK_TOKEN})
        response = self.s.post(self.url_signinbyfb, data=userdata, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)


class Test_Recovery_Password(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_Recovery_Password, self).__init__(*a, **kw)
        self.command_recovery_password = 'auth/recovery'
        self.url_recovery_password = '{}/{}'.format(HOST, self.command_recovery_password)
        self.s = requests.Session()

    def test_01_recovered_password_successfully(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        userdata = json.dumps({"email": EMAIL})
        response = self.s.post(self.url_recovery_password, data=userdata, headers=headers)
        reset_token = response.headers['reset_token']

        self.assertEqual(response.status_code, MAIL_SENT)

        self.command_reset_password = 'auth/reset'
        self.url_reset_password = '{}/{}'.format(HOST, self.command_reset_password)
        userdata = json.dumps({"token": reset_token, "password": PSW, "password_confirmation": PSW})
        response = self.s.post(self.url_reset_password, data=userdata, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)


class Test_Refresh_Token(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_Refresh_Token, self).__init__(*a, **kw)
        self.command_refresh_token = 'auth/refresh'
        self.url_refresh_token = '{}/{}'.format(HOST, self.command_refresh_token)
        self.s = requests.Session()

    def test_01_refreshed_token_successfully(self):

        token, index = test_authorization()
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        response = self.s.get(self.url_refresh_token, headers=headers)
        newToken = response.headers['Authorization']

        self.assertNotEqual(token, newToken)
        self.assertEqual(response.status_code, MAIL_SENT)

if __name__ == '__main__':
    unittest.main()