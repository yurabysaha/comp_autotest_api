import json
import requests
import unittest
from authorization import test_authorization
from baseSettings import *


class ATest_001_All_tags(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(ATest_001_All_tags, self).__init__(*a, **kw)
        self.s = requests.Session()
        self.token, index = test_authorization()
        self.headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': self.token}

    def test_01_all_tags_opened(self):

        self.command_all_tags = 'management/tags'
        self.url_all_tags = '{}/{}'.format(HOST, self.command_all_tags)
        response = self.s.get(self.url_all_tags, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)

    def test_02_test_pagination(self):

        self.command_all_tags = 'management/tags'
        page = 'page=1&limit=10'
        self.url_all_tags = '{}/{}?{}'.format(HOST, self.command_all_tags, page)
        response = self.s.get(self.url_all_tags, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)
        page1data = json.loads(response.content)['data']

        page = 'page=2&limit=10'
        self.url_all_tags = '{}/{}?{}'.format(HOST, self.command_all_tags, page)
        response = self.s.get(self.url_all_tags, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)
        self.assertNotEqual(page1data, json.loads(response.content)['data'])


class Test_002_tag_Show(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_002_tag_Show, self).__init__(*a, **kw)
        self.s = requests.Session()
        self.token, self.index = test_authorization()
        self.headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': self.token}

    def test_01_tag_page_showed_correctly(self):

        self.command_all_tags = 'management/tags'
        self.url_all_tags = '{}/{}'.format(HOST, self.command_all_tags)
        tags = self.s.get(self.url_all_tags, headers=self.headers)
        m = json.loads(tags.content)
        index = int(m['data'][0]['id'])

        self.command_tag_show = 'management/tags/show'
        self.url_tag_show = '{}/{}/{}'.format(HOST, self.command_tag_show, index)
        response = self.s.get(self.url_tag_show, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)

    def test_02_tag_page_short_version_showed_correctly(self):

        self.command_all_tags = 'management/tags'
        self.url_all_tags = '{}/{}'.format(HOST, self.command_all_tags)
        tags = self.s.get(self.url_all_tags, headers=self.headers)
        m = json.loads(tags.content)
        index = int(m['data'][0]['id'])

        self.command_tag_show = 'management/tags/show'
        self.url_tag_show = '{}/{}/{}'.format(HOST, self.command_tag_show, index)
        response = self.s.get(self.url_tag_show, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)


class Test_003_tags_Creation(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_003_tags_Creation, self).__init__(*a, **kw)
        self.s = requests.Session()
        self.token, self.index = test_authorization()
        self.headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': self.token}

    def test_01_tags_created_correctly(self):

        self.command_tags_create = 'management/tags/create'
        self.url_tags_create = '{}/{}'.format(HOST, self.command_tags_create)
        userdata = json.dumps({"name": "TestName", "matching_coefficient": 0, "is_special": False})
        response = self.s.post(self.url_tags_create, data=userdata, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)


class Test_004_tags_Deleting(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_004_tags_Deleting, self).__init__(*a, **kw)
        self.s = requests.Session()
        self.token, self.index = test_authorization()
        self.headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': self.token}

    def test_01_tags_deleted_correctly(self):

        self.command_tags_create = 'management/tags/create'
        self.url_tags_create = '{}/{}'.format(HOST, self.command_tags_create)
        userdata = json.dumps({"name": "TestName", "matching_coefficient": 0, "is_special": False})

        response = self.s.post(self.url_tags_create, data=userdata, headers=self.headers)
        cont = json.loads(response.content)
        identifier = cont['id']

        self.assertEqual(response.status_code, SUCCESS)

        self.command_tags_update = 'management/tags/update'
        self.url_tags_update = '{}/{}/{}'.format(HOST, self.command_tags_update, identifier)
        userdata = json.dumps({"name": "tagsTest"})
        response = self.s.patch(self.url_tags_update, data=userdata, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)

        self.command_tags_delete = 'management/tags/delete'
        self.url_tags_delete = '{}/{}/{}'.format(HOST, self.command_tags_delete, identifier)
        response = self.s.delete(self.url_tags_delete, headers=self.headers)

        self.assertEqual(response.status_code, NO_CONTENT)

    def test_02_not_deleted_because_of_alphabetical_id(self):

        self.command_tags_delete = 'management/tags/delete'
        index = 'b'
        self.url_tags_delete = '{}/{}/{}'.format(HOST, self.command_tags_delete, index)
        response = self.s.delete(self.url_tags_delete, headers=self.headers)

        self.assertEqual(response.status_code, WRONGID)

    def test_03_tags_cant_be_deleted_because_id_doesnt_exist(self):

        self.command_tags_delete = 'management/tags/delete'
        index = 900
        self.url_tags_delete = '{}/{}/{}'.format(HOST, self.command_tags_delete, index)
        response = self.s.delete(self.url_tags_delete, headers=self.headers)

        self.assertEqual(response.status_code, BADDATA)


if __name__ == '__main__':
    unittest.main()
