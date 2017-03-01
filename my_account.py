import json
import requests
import unittest
from authorization import test_authorization
from baseSettings import *
import time


class Test_001_My_Profile_View(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_001_My_Profile_View, self).__init__(*a, **kw)
        self.command_profile_view = 'me'
        self.url_profile_view = '{}/{}'.format(HOST, self.command_profile_view)
        self.s = requests.Session()

    def test_01_user_profile_opened(self):

        token, index = test_authorization()
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        response = self.s.get(self.url_profile_view, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)

    def test_02_user_profile_not_opened_because_empty_token(self):

        token = ""
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        response = self.s.get(self.url_profile_view, headers=headers)

        self.assertEqual(response.status_code, BADDATA)

    def test_03_user_profile_not_opened_because_wrong_token(self):

        token = "dfgetgergergergerg"
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        response = self.s.get(self.url_profile_view, headers=headers)

        self.assertEqual(response.status_code, BADDATA)

    def test_04_user_profile_not_opened_because_expired_token(self):

        token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjE0MiwiaXNzIjoiaHR0cDpcL1wvNTQuOTMuODEuMTY5XC9hcGlcL3YxXC9hdXRoXC9zaWdudXAiLCJpYXQiOjE0ODM0NTQ0NzcsImV4cCI6MTQ4MzQ1ODA3NywibmJmIjoxNDgzNDU0NDc3LCJqdGkiOiJkZTAwMWQ5YmUxMGNhYjA1M2QzODE1YjhhNTMyNmYwMyJ9.Zrv6bt85tvKXvMLiB57poGbQvCJ7K1ghF0pjrG-EyfU"
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        response = self.s.get(self.url_profile_view, headers=headers)

        self.assertEqual(response.status_code, EXPIRED_TOKEN)


class Test_002_My_Profile_Edit(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_002_My_Profile_Edit, self).__init__(*a, **kw)
        self.command_profile_edit = 'me/update'
        self.url_profile_edit = '{}/{}'.format(HOST, self.command_profile_edit)
        self.s = requests.Session()

    def test_01_user_profile_edited(self):

        token, index = test_authorization()
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        edited_name = "EditedName"
        userdata = json.dumps({"full_name": edited_name})
        response = self.s.patch(self.url_profile_edit, data=userdata, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)
        self.assertEqual(json.loads(response.content)["full_name"], edited_name)


class Test_003_My_Profile_Change_Password(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_003_My_Profile_Change_Password, self).__init__(*a, **kw)
        self.command_sign_in = 'auth/signin'
        self.command_change_password = 'me/change-password'
        self.url_change_passsword = '{}/{}'.format(HOST, self.command_change_password)
        self.s = requests.Session()


    def test_01_user_change_password_successfully(self):

        self.url_sign_in = '{}/{}'.format(HOST, self.command_sign_in)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        userdata = json.dumps({"email": EMAIL, "password": PSW})
        response = self.s.post(self.url_sign_in, data=userdata, headers=headers)
        auth_token = response.headers['Authorization']

        self.assertEqual(response.status_code, SUCCESS)

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': auth_token}
        userdata = json.dumps({ "old_password": PSW, "new_password": PSW, "new_password_confirmation": PSW})
        response = self.s.post(self.url_change_passsword, data=userdata, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)

    def test_02_user_change_password_wrong_old_password(self):

        self.url_sign_in = '{}/{}'.format(HOST, self.command_sign_in)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        passvalue = "string"
        userdata = json.dumps({"email": EMAIL, "password": PSW})
        response = self.s.post(self.url_sign_in, data=userdata, headers=headers)
        auth_token = response.headers['Authorization']

        self.assertEqual(response.status_code, SUCCESS)

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': auth_token}
        userdata = json.dumps({ "old_password": "blalalala", "new_password": passvalue, "new_password_confirmation": passvalue})
        response = self.s.post(self.url_change_passsword, data=userdata, headers=headers)

        self.assertEqual(response.status_code, BADDATA)

    def test_03_user_change_password_empty_old_password(self):

        self.url_sign_in = '{}/{}'.format(HOST, self.command_sign_in)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        passvalue = "string"
        userdata = json.dumps({"email": EMAIL, "password": PSW})
        response = self.s.post(self.url_sign_in, data=userdata, headers=headers)
        auth_token = response.headers['Authorization']

        self.assertEqual(response.status_code, SUCCESS)

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': auth_token}
        userdata = json.dumps({ "old_password": "", "new_password": passvalue, "new_password_confirmation": passvalue})
        response = self.s.post(self.url_change_passsword, data=userdata, headers=headers)

        self.assertEqual(response.status_code, BADDATA)


class Test_004_My_Profile_LogOut(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_004_My_Profile_LogOut, self).__init__(*a, **kw)
        self.command_log_out = 'me/logout'
        self.command_sign_in = 'auth/signin'
        self.url_log_out = '{}/{}'.format(HOST, self.command_log_out)
        self.s = requests.Session()

    def test_01_user_log_out_successfully(self):

        self.url_sign_in = '{}/{}'.format(HOST, self.command_sign_in)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        userdata = json.dumps({"email": EMAIL, "password": PSW})
        response = self.s.post(self.url_sign_in, data=userdata, headers=headers)
        auth_token = response.headers['Authorization']

        self.assertEqual(response.status_code, SUCCESS)

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': auth_token}
        response = self.s.get(self.url_log_out, headers=headers)

        self.assertEqual(response.status_code, NO_CONTENT)


if __name__ == '__main__':
    unittest.main()
