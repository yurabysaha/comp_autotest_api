import json
import requests
import unittest
from baseSettings import *


class Test_004_Search(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_004_Search, self).__init__(*a, **kw)
        self.command_search = 'search'
        self.searchQuery = 'searchQuery'
        self.searchvalue = 'klip'
        self.s = requests.Session()
        self.url_search = '{}/{}?{}={}'.format(HOST, self.command_search, self.searchQuery, self.searchvalue)

    def test_01_search_successfully(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        response = self.s.get(self.url_search, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)

    def test_02_search_successfully(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        response = self.s.get(self.url_search, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)


class Test_004_Search1(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_004_Search1, self).__init__(*a, **kw)
        self.command_search = 'search'
        self.searchQuery = 'searchQuery'
        self.searchvalue = 'klip'
        self.isocode1 = 'isocode1'
        self.isocode1value = 'sv'
        self.s = requests.Session()
        self.url_search = '{}/{}?{}={}&{}={}'.format(HOST, self.command_search, self.searchQuery, self.searchvalue, self.isocode1, self.isocode1value)

    def test_01_search_successfully(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        response = self.s.get(self.url_search, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)


class Test_004_Search2(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_004_Search2, self).__init__(*a, **kw)
        self.command_search = 'search'
        self.searchQuery = 'searchQuery'
        self.searchvalue = 'klip'
        self.isocode1 = 'isocode1'
        self.isocode1value = 'sv'
        self.page = 'page'
        self.pagevalue = '1'
        self.s = requests.Session()
        self.url_search = '{}/{}?{}={}&{}={}&{}={}'.format(HOST, self.command_search, self.searchQuery, self.searchvalue, self.isocode1, self.isocode1value, self.page, self.pagevalue)

    def test_01_search_successfully(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        response = self.s.get(self.url_search, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)


class Test_004_Search3(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_004_Search3, self).__init__(*a, **kw)
        self.command_search = 'search'
        self.searchQuery = 'searchQuery'
        self.searchvalue = 'klip'
        self.isocode1 = 'isocode1'
        self.isocode1value = 'sv'
        self.page = 'page'
        self.pagevalue = '1'
        self.limit = 'limit'
        self.limitvalue = '1'
        self.s = requests.Session()
        self.url_search = '{}/{}?{}={}&{}={}&{}={}&{}={}'.format(HOST, self.command_search, self.searchQuery, self.searchvalue, self.isocode1, self.isocode1value, self.page, self.pagevalue, self.limit, self.limitvalue)

    def test_01_search_successfully(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        response = self.s.get(self.url_search, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)


class Test_004_Search4(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_004_Search4, self).__init__(*a, **kw)
        self.s = requests.Session()
        self.command_search = 'search'
        self.searchQuery = 'searchQuery'
        self.searchvalue = 'klip'
        self.isocode1 = 'isocode1'
        self.isocode1value = 'sv'
        self.page = 'page'
        self.pagevalue = '1'
        self.limit = 'limit'
        self.limitvalue = '1'
        self.category_id = 'category_id'
        self.category_id_value = '55555'
        self.url_search = '{}/{}?{}={}&{}={}&{}={}&{}={}&{}={}'.format(HOST, self.command_search, self.searchQuery, self.searchvalue, self.isocode1, self.isocode1value, self.page, self.pagevalue, self.limit, self.limitvalue, self.category_id, self.category_id_value)

    def test_01_search_successfully(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        response = self.s.get(self.url_search, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)


class Test_004_Search5(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_004_Search5, self).__init__(*a, **kw)
        self.command_search = 'search'
        self.s = requests.Session()
        self.url_search = '{}/{}'.format(HOST, self.command_search)

    def test_01_search_successfully(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        response = self.s.get(self.url_search, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)


class Test_004_Search6(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_004_Search6, self).__init__(*a, **kw)
        self.s = requests.Session()
        self.command_search = 'search'
        self.searchQuery = 'searchQuery'
        self.searchvalue = 'klip'
        self.isocode1 = 'isocode1'
        self.isocode1value = 'sv'
        self.page = 'page'
        self.pagevalue = '1'
        self.limit = 'limit'
        self.limitvalue = '1'
        self.category_id = 'category_id'
        self.category_id_value = '55555'
        self.withRelations = 'withRelations'
        self.withRelations_value = 'test'
        self.url_search = '{}/{}'.format(HOST, self.command_search, self.searchQuery, self.searchvalue, self.isocode1, self.isocode1value, self.page, self.pagevalue, self.limit, self.limitvalue, self.category_id, self.category_id_value, self.withRelations, self.withRelations_value)

    def test_01_search_successfully(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        response = self.s.get(self.url_search, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)

        act = json.loads(response.content)
        elem = act['data'][1]['id']

        self.assertIsNotNone(elem)


if __name__ == '__main__':
    unittest.main()
