import json
import requests
import unittest

import time
from authorization import test_authorization

DEFAULT_HEADER = 'application/json'

SUCCESS = 200
BADREQUEST = 400
ADDED = 201
UNAUTHORIZED = 401
UPGRADE_REQUIRED = 426
FORBIDDEN = 403
NOTFOUND = 404
BADDATA = 422
WRONGID = 500
ACTION_IS_DONE = 204
DETACHED = 202




TAN = 9999
FIRSTNAME = "Oleg"
LASTNAME = time.strftime("%d/%m/%Y"+"%H:%M:%S")+"@"+"test.com"
EMAIL = 'biziliavv@gmail.com'
PSW = "123456"
host = '54.93.81.169/api/v1'

class Test_004_All_tags(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_004_All_tags, self).__init__(*a, **kw)
        self.host = host
        self.command_all_tags = 'management/tags'


        self.url_all_tags = 'http://{}/{}'.format(self.host, self.command_all_tags)


    def test_01_all_tags_opened(self):
        with open('USER_DATA.json') as data_file:
            data = json.load(data_file)
        s = requests.Session()
        token, index = test_authorization()
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        response2 = s.get(self.url_all_tags, headers=headers)
        print response2
        self.assertEqual(response2.status_code, SUCCESS)

class Test_004_tag_Show(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_004_tag_Show, self).__init__(*a, **kw)



    def test_01_tag_page_showed_correctly(self):
        with open('USER_DATA.json') as data_file:
            data = json.load(data_file)
        s = requests.Session()
        token, index = test_authorization()
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        self.host = host
        self.command_all_tags = 'management/tags'



        self.url_all_tags = 'http://{}/{}'.format(self.host, self.command_all_tags)
        tags = s.get(self.url_all_tags, headers=headers)
        m = json.loads(tags.content)

        print m
        print m['data'][0]
        index = int(m['data'][0]['id'])
        print index
        self.host = host
        self.command_tag_show = 'management/tags/show'

        self.url_tag_show = 'http://{}/{}/{}'.format(self.host, self.command_tag_show, index)
        response2 = s.get(self.url_tag_show, headers=headers)
        print response2
        self.assertEqual(response2.status_code, SUCCESS)
    def test_01_tag_page_short_version_showed_correctly(self):
        with open('USER_DATA.json') as data_file:
            data = json.load(data_file)
        s = requests.Session()
        token, index = test_authorization()
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        self.host = host
        self.command_all_tags = 'management/tags'


        self.url_all_tags = 'http://{}/{}'.format(self.host, self.command_all_tags)
        tags = s.get(self.url_all_tags, headers=headers)
        m = json.loads(tags.content)

        print m
        print m['data'][0]
        index = int(m['data'][0]['id'])
        print index
        self.host = host
        self.command_tag_show = 'management/tags/show'

        self.url_tag_show = 'http://{}/{}/{}'.format(self.host, self.command_tag_show, index)
        response2 = s.get(self.url_tag_show, headers=headers)
        print response2
        self.assertEqual(response2.status_code, SUCCESS)

class Test_004_tags_Creation(unittest.TestCase):
    def __init__(self, *a, **kw):
        super(Test_004_tags_Creation, self).__init__(*a, **kw)

    def test_01_tags_created_correctly(self):
        with open('USER_DATA.json') as data_file:
            data = json.load(data_file)
        s = requests.Session()
        time.sleep(5)
        token, index = test_authorization()
        time.sleep(5)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        self.host = host
        self.command_tags_create = 'management/tags/create'


        self.url_tags_create = 'http://{}/{}'.format(self.host, self.command_tags_create)
        userdata = json.dumps({"name": "TestName", "matching_coefficient": 0, "is_special": False})

        response2 = s.post(self.url_tags_create, data=userdata, headers=headers)

        self.assertEqual(response2.status_code, SUCCESS)


class Test_004_tags_Deleting(unittest.TestCase):
    def __init__(self, *a, **kw):
        super(Test_004_tags_Deleting, self).__init__(*a, **kw)

    def test_01_tags_deleted_correctly(self):
        with open('USER_DATA.json') as data_file:
            data = json.load(data_file)
        s = requests.Session()
        time.sleep(5)
        token, index = test_authorization()
        time.sleep(5)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        self.host = host
        self.command_tags_create = 'management/tags/create'

        self.url_tags_create = 'http://{}/{}'.format(self.host, self.command_tags_create)
        userdata = json.dumps({"name": "TestName", "matching_coefficient": 0, "is_special": False})

        response2 = s.post(self.url_tags_create, data=userdata, headers=headers)
        cont = json.loads(response2.content)

        identifier = cont['id']
        self.assertEqual(response2.status_code, SUCCESS)

        self.host = host
        self.command_tags_update = 'management/tags/update'

        self.url_tags_update = 'http://{}/{}/{}'.format(self.host, self.command_tags_update, identifier)
        userdata = json.dumps({"name": "tagsTest"})
        response2 = s.patch(self.url_tags_update, data=userdata, headers=headers)
        print response2
        self.assertEqual(response2.status_code, SUCCESS)

        self.host = host
        self.command_tags_delete = 'management/tags/delete'

        self.url_tags_delete = 'http://{}/{}/{}'.format(self.host, self.command_tags_delete, identifier)
        response2 = s.delete(self.url_tags_delete, headers=headers)
        print response2
        self.assertEqual(response2.status_code, SUCCESS)

    def test_01_not_deleted_because_of_alphabetical_id(self):
        with open('USER_DATA.json') as data_file:
            data = json.load(data_file)
        s = requests.Session()
        time.sleep(5)
        token, index = test_authorization()
        time.sleep(5)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}

        self.host = host
        self.command_tags_delete = 'management/tags/delete'
        index = 'b'
        self.url_tags_delete = 'http://{}/{}/{}'.format(self.host, self.command_tags_delete, index)
        response2 = s.delete(self.url_tags_delete, headers=headers)
        print response2
        self.assertEqual(response2.status_code, WRONGID)

    def test_01_tags_cant_be_deleted_because_id_doesnt_exist(self):
        with open('USER_DATA.json') as data_file:
            data = json.load(data_file)
        s = requests.Session()
        time.sleep(5)
        token, index = test_authorization()
        time.sleep(5)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}

        self.host = host
        self.command_tags_delete = 'management/tags/delete'
        index = 900
        self.url_tags_delete = 'http://{}/{}/{}'.format(self.host, self.command_tags_delete, index)
        response2 = s.delete(self.url_tags_delete, headers=headers)
        print response2
        self.assertEqual(response2.status_code, BADDATA)




if __name__ == '__main__':
    unittest.main()
