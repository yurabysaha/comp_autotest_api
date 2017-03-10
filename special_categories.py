import json
import requests
import unittest
from authorization import authorization
from baseSettings import *


class Test_001_get_special_categories(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_001_get_special_categories, self).__init__(*a, **kw)
        self.s = requests.Session()
        self.token, self.index = authorization()
        self.headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': self.token}

    def test_01_all_special_categories_opened(self):

        self.command_get_categories = 'categories'
        self.url_all_special_categories = '{}/{}'.format(HOST, self.command_get_categories)
        response = self.s.get(self.url_all_special_categories, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)

if __name__ == '__main__':
    unittest.main()
