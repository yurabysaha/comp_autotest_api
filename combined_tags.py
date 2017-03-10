import json
import requests
import unittest
from authorization import authorization
from baseSettings import *


class Test_001_get_combined_tags(unittest.TestCase):
    def __init__(self, *a, **kw):
        super(Test_001_get_combined_tags, self).__init__(*a, **kw)
        self.s = requests.Session()
        self.token, self.index = authorization()
        self.headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': self.token}

# GET /management/combined-tags
    def test_01_get_combined_tags(self):
        self.command_all_tags = 'management/combined-tags'
        relation = "relations[]=tag"
        self.url_all_tags = '{}/{}?{}'.format(HOST, self.command_all_tags, relation)
        response = self.s.get(self.url_all_tags, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)

# GET /management/combined-tags
    def test_02_get_combined_tags_with_categories(self):
        self.command_all_tags = 'management/combined-tags'
        relation = "relations[]=categories"
        self.url_all_tags = '{}/{}?{}'.format(HOST, self.command_all_tags, relation)
        response = self.s.get(self.url_all_tags, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)

# GET /management/combined-tags/show/{id}
    def test_03_get_combined_tags_show(self):
        self.command_all_tags = 'management/combined-tags/show'
        self.url_all_tags = '{}/{}/{}'.format(HOST, self.command_all_tags, 128)
        response = self.s.get(self.url_all_tags, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)

# POST /management/combined-tags/create

# DELETE /management/combined-tags/delete/{id}