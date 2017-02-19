import unittest
import requests
import json
import time
from baseSettings import *


def test_authorization():
        s = requests.Session()
        command_signin = 'auth/signin'
        url_signin = '{}/{}'.format(HOST, command_signin)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}

        #email_value = time.strftime("%d%m%Y" + "%H%M%S") + "@" + "test.com"

        userdata = json.dumps({ "email": EMAIL, "password": PSW})
        response = s.post(url_signin, data=userdata, headers=headers)
        time.sleep(2)
        auth_token = response.headers['Authorization']
        index = json.loads(response.content)['id']

        return (auth_token, index)

if __name__ == '__main__':
    unittest.main()

