import json
import requests
import unittest
from baseSettings import *


class Test_001_All_businesses(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_001_All_businesses, self).__init__(*a, **kw)
        self.command_all_businesses = 'businesses'
        self.url_all_businesses = '{}/{}'.format(HOST, self.command_all_businesses)
        self.s = requests.Session()

    def test_01_all_businesses_opened(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        response = self.s.get(self.url_all_businesses, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)


class Test_002_business_Show(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_002_business_Show, self).__init__(*a, **kw)
        self.s = requests.Session()

    def test_01_business_page_showed_correctly(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        self.command_all_businesses = 'businesses'

        self.url_all_businesses = '{}/{}'.format(HOST, self.command_all_businesses)
        businesses = self.s.get(self.url_all_businesses, headers=headers)
        m = json.loads(businesses.content)
        id = int(m['data'][0]['id'])

        self.command_business_show = 'businesses/show'
        self.url_business_show = '{}/{}/{}'.format(HOST, self.command_business_show, id)
        response = self.s.get(self.url_business_show, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)
        self.assertEqual(json.loads(response.content)['id'], id)


if __name__ == '__main__':
    unittest.main()
