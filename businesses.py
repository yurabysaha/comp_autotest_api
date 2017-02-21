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


class Test_002_Business_Show(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_002_Business_Show, self).__init__(*a, **kw)
        self.s = requests.Session()
        self.headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}

    def test_01_business_page_showed_correctly(self):

        self.command_all_businesses = 'businesses'
        self.url_all_businesses = '{}/{}'.format(HOST, self.command_all_businesses)
        businesses = self.s.get(self.url_all_businesses, headers=self.headers)
        m = json.loads(businesses.content)
        id = int(m['data'][0]['id'])

        self.command_business_show = 'businesses/show'
        self.url_business_show = '{}/{}/{}'.format(HOST, self.command_business_show, id)
        response = self.s.get(self.url_business_show, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)
        self.assertEqual(json.loads(response.content)['id'], id)

    def test_02_business_page_showed_withRelations_partner(self):

        self.command_all_businesses = 'businesses'
        self.url_all_businesses = '{}/{}'.format(HOST, self.command_all_businesses)
        businesses = self.s.get(self.url_all_businesses, headers=self.headers)
        m = json.loads(businesses.content)
        id = int(m['data'][0]['id'])
        relation = 'withRelations=partner'
        self.command_business_show = 'businesses/show'
        self.url_business_show = '{}/{}/{}?{}'.format(HOST, self.command_business_show, id, relation)
        response = self.s.get(self.url_business_show, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)
        response = json.loads(response.content)
        self.assertEqual(response['id'], id)
        self.assertEqual('partner' in response, True)

    def test_03_business_page_showed_withRelations_offers(self):
        self.command_all_businesses = 'businesses'
        self.url_all_businesses = '{}/{}'.format(HOST, self.command_all_businesses)
        businesses = self.s.get(self.url_all_businesses, headers=self.headers)
        m = json.loads(businesses.content)
        id = int(m['data'][0]['id'])
        relation = 'withRelations=offers'
        self.command_business_show = 'businesses/show'
        self.url_business_show = '{}/{}/{}?{}'.format(HOST, self.command_business_show, id, relation)
        response = self.s.get(self.url_business_show, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)
        response = json.loads(response.content)
        self.assertEqual(response['id'], id)
        self.assertEqual('offers' in response, True)

    def test_04_business_page_showed_withRelations_images(self):
        self.command_all_businesses = 'businesses'
        self.url_all_businesses = '{}/{}'.format(HOST, self.command_all_businesses)
        businesses = self.s.get(self.url_all_businesses, headers=self.headers)
        m = json.loads(businesses.content)
        id = int(m['data'][0]['id'])
        relation = 'withRelations=images'
        self.command_business_show = 'businesses/show'
        self.url_business_show = '{}/{}/{}?{}'.format(HOST, self.command_business_show, id, relation)
        response = self.s.get(self.url_business_show, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)
        response = json.loads(response.content)
        self.assertEqual(response['id'], id)
        self.assertEqual('images' in response, True)


if __name__ == '__main__':
    unittest.main()
