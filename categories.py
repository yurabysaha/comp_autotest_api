import json
from ConfigParser import SafeConfigParser
import requests
import unittest
from authorization import authorization
from baseSettings import *


class Test_001_category_crud(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_001_category_crud, self).__init__(*a, **kw)
        self.s = requests.Session()
        self.config = SafeConfigParser()
        self.token, self.index = authorization()
        self.headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': self.token}

    def test_01_category_create(self):

        self.command_category_create = 'management/categories/create'
        self.url_category_create = '{}/{}'.format(HOST, self.command_category_create)
        userdata = json.dumps({"parent_id": 3, "is_last": "false", "title": "string", "description": "string"})
        response = self.s.post(self.url_category_create, data=userdata, headers=self.headers)

        self.config.read('config.ini')
        self.config.set('for_test', 'category_id', str(json.loads(response.content)['id']))
        with open('config.ini', 'w') as f:
            self.config.write(f)

        self.assertEqual(response.status_code, SUCCESS)

    def test_02_category_update(self):
        self.command_category_update = 'management/categories/update'

        self.config.read('config.ini')
        category_id = self.config.getint('for_test', 'category_id')
        self.isocode = 'isocode1'
        self.isocode_value = 'en'
        self.url_category_update = '{}/{}/{}?{}={}'.format(HOST, self.command_category_update,
                                                           category_id, self.isocode,
                                                            self.isocode_value)
        new_title = 'categoryTest'
        userdata = json.dumps({"title": new_title})
        response = self.s.patch(self.url_category_update, data=userdata, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)
        self.assertEqual(json.loads(response.content)['title'], new_title)

    def test_03_category_show(self):

        self.config.read('config.ini')
        category_id = self.config.getint('for_test', 'category_id')

        self.command_category_show = 'categories/show'
        self.url_category_show = '{}/{}/{}'.format(HOST, self.command_category_show, category_id)
        response = self.s.get(self.url_category_show, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)

    def test_04_category_delete(self):

        self.config.read('config.ini')
        category_id = self.config.getint('for_test', 'category_id')

        self.command_category_delete = 'management/categories/delete'
        self.url_category_delete = '{}/{}/{}'.format(HOST, self.command_category_delete, category_id)
        response = self.s.delete(self.url_category_delete, headers=self.headers)

        self.assertEqual(response.status_code, NO_CONTENT)


class Test_002_All_categories(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_002_All_categories, self).__init__(*a, **kw)
        self.command_all_categories = 'categories'
        self.url_all_categories = '{}/{}'.format(HOST, self.command_all_categories)
        self.s = requests.Session()

    def test_01_all_categories_opened(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        response = self.s.get(self.url_all_categories, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)


class Test_003_category_Show(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_003_category_Show, self).__init__(*a, **kw)
        self.s = requests.Session()
        self.headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}

    def test_01_category_page_showed_correctly(self):

        self.command_all_categories = 'categories'
        self.isocode = 'isocode1'
        self.isocode_value = 'sv'
        self.parent_id = 'parent_id'
        self.parent_id_value = 'null'
        self.page = 'page'
        self.page_number = '1'
        self.page_limit = 'limit'
        self.page_limit_value = '1000'
        self.url_all_categories = '{}/{}?{}={}&{}={}&{}={}&{}={}'.format(HOST, self.command_all_categories,
                                                                         self.parent_id, self.parent_id_value,
                                                                         self.isocode, self.isocode_value, self.page,
                                                                         self.page_number, self.page_limit,
                                                                         self.page_limit_value)
        categories = self.s.get(self.url_all_categories, headers=self.headers)
        m = json.loads(categories.content)
        index = int(m['data'][0]['id'])

        self.command_category_show = 'categories/show'
        self.url_category_show = '{}/{}/{}'.format(HOST, self.command_category_show, index)
        response = self.s.get(self.url_category_show, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)

    def test_02_category_page_short_version_showed_correctly(self):

        self.command_all_categories = 'categories'
        self.url_all_categories = '{}/{}'.format(HOST, self.command_all_categories)
        categories = self.s.get(self.url_all_categories, headers=self.headers)
        m = json.loads(categories.content)
        index = int(m['data'][0]['id'])

        self.command_category_show = 'categories/show'
        self.url_category_show = '{}/{}/{}'.format(HOST, self.command_category_show, index)
        response = self.s.get(self.url_category_show, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)

    def test_03_category_show_withRelations(self):

        self.command_all_categories = 'categories'
        self.url_all_categories = '{}/{}'.format(HOST, self.command_all_categories)
        categories = self.s.get(self.url_all_categories, headers=self.headers)
        m = json.loads(categories.content)
        index = int(m['data'][0]['id'])
	keys = ['offers','parent','children','offersInCategory','favoriteOffers','tags','specialCategories']
        for k in keys:
            self.command_category_show = 'categories/show'
            self.url_category_show = '{}/{}/{}?withRelations={}'.format(HOST, self.command_category_show, index, k)
            response = self.s.get(self.url_category_show, headers=self.headers)

            self.assertEqual(response.status_code, SUCCESS)
            response = json.loads(response.content)
            self.assertEqual(k in response, True)


class Test_004_Tag_Attaching_To_Category(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_004_Tag_Attaching_To_Category, self).__init__(*a, **kw)
        self.s = requests.Session()

    def test_01_attaching_tags_to_category(self):
        token, index = authorization()

        self.command_category_create = 'management/categories/create'

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        self.url_category_create = '{}/{}'.format(HOST, self.command_category_create)
        userdata = json.dumps({"parent_id": 3, "is_last": "false", "title": "string", "description": "string"})
        response = self.s.post(self.url_category_create, data=userdata, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)

        index = json.loads(response.content)['id']

        self.command_tags_create = 'management/tags/create'
        self.url_tags_create = '{}/{}'.format(HOST, self.command_tags_create)
        userdata = json.dumps({"name": "TestName"})

        response = self.s.post(self.url_tags_create, data=userdata, headers=headers)
        identifier = json.loads(response.content)['id']

        self.assertEqual(response.status_code, SUCCESS)

        self.command_tag_attaching_to_category = 'management/categories/attach/tag'
        self.category_id = 'category_id'
        self.tag_id = 'tag_id'
        self.tag_type = 'tag_type=App\\Tag'
        self.matching_criteria = 'matching_criteria=areWordsSimilar'
        self.importance = 'importance=medium'

        self.url_tag_attaching_to_category = '{}/{}?{}={}&{}={}&{}&{}&{}'.format(HOST, self.command_tag_attaching_to_category,
                                                                              self.category_id, index, self.tag_id,
                                                                              identifier, self.tag_type, self.matching_criteria,
                                                                              self.importance)
        response = self.s.post(self.url_tag_attaching_to_category, headers=headers)

        self.assertEqual(response.status_code, NO_CONTENT)

        self.command_tag_detaching_to_category = 'management/categories/detach/tag'
        self.url_tag_detaching_to_category = '{}/{}?{}={}&{}={}&{}'.format(HOST, self.command_tag_detaching_to_category,
                                                                           self.category_id, index, self.tag_id,
                                                                           identifier, self.tag_type)
        response = self.s.post(self.url_tag_detaching_to_category, headers=headers)

        self.assertEqual(response.status_code, NO_CONTENT)

        self.command_category_delete = 'management/categories/delete'
        self.url_category_delete = '{}/{}/{}'.format(HOST, self.command_category_delete, index)
        response = self.s.delete(self.url_category_delete, headers=headers)

        self.assertEqual(response.status_code, NO_CONTENT)


if __name__ == '__main__':
    unittest.main()
