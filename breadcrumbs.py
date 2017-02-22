import json
import requests
import unittest
from baseSettings import *


# GET /breadcrumbs
class Test_001_get_breadcrumbs(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_001_get_breadcrumbs, self).__init__(*a, **kw)
        self.s = requests.Session()
        self.headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}

    def test_01_all_businesses_opened(self):
        self.command_get_breadcrumbs = 'breadcrumbs'
        category_id = 1
        self.url_get_breadcrumbs = '{}/{}?{}'.format(HOST, self.command_get_breadcrumbs, 'id='+str(category_id))
        response = self.s.get(self.url_get_breadcrumbs, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)
        response = json.loads(response.content)
        self.assertEqual(response[0]['id'], category_id)
