import json
from ConfigParser import SafeConfigParser

import requests
import unittest
import random
from baseSettings import *
import time
from authorization import authorization


        # --------------------- MANAGEMENT USERS ---------------------------#


# GET /management/users
class Test_001_All_users(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_001_All_users, self).__init__(*a, **kw)
        self.command_all_users = 'management/users'
        self.url_all_users = '{}/{}'.format(HOST, self.command_all_users)
        self.s = requests.Session()

    def test_01_all_users_opened(self):
        token, index = authorization()
        time.sleep(3)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        response = self.s.get(self.url_all_users, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)


# GET /management/users/show/{id}
class Test_002_user_Show(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_002_user_Show, self).__init__(*a, **kw)
        self.s = requests.Session()

    def test_01_user_page_showed_correctly(self):

        token, index = authorization()
        time.sleep(3)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        self.command_all_users = 'management/users'
        self.url_all_users = '{}/{}'.format(HOST, self.command_all_users)
        users = self.s.get(self.url_all_users, headers=headers)

        self.command_user_show = 'management/users/show'
        self.url_user_show = '{}/{}/{}'.format(HOST, self.command_user_show, index)
        response = self.s.get(self.url_user_show, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)


# POST /management/users/create
class Test_003_user_Creation(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_003_user_Creation, self).__init__(*a, **kw)
        self.s = requests.Session()

    def test_01_user_created_correctly(self):

        token, index = authorization()
        time.sleep(3)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        self.command_user_create = 'management/users/create'
        self.url_user_create = '{}/{}'.format(HOST, self.command_user_create)
        words = ["python", "jumble", "easy", "difficult", "answer", "xylophone"]
        newValue = random.choice(words)
        nameunique = "testuser" + time.strftime("%d%m%Y" + "%H%M%S") + "@" + random.choice(words) + ".com"
        email_value = time.strftime("%d%m%Y" + "%H%M%S") + "@" + "test.com"
        userdata = json.dumps({"full_name": newValue, "email": email_value, "password": "12345678", "password_confirmation": "12345678", "birthday": "1990-20-06", "gender": "male"})

        response = self.s.post(self.url_user_create, data=userdata, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)

    def test_02_user_not_created_empty_values(self):

        token, index = authorization()
        time.sleep(3)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        self.command_user_create = 'management/users/create'
        self.url_user_create = '{}/{}'.format(HOST, self.command_user_create)
        userdata = json.dumps({"full_name": "", "email": "", "password": "", "password_confirmation": "", "birthday": ""})
        response = self.s.post(self.url_user_create, data=userdata, headers=headers)

        self.assertEqual(response.status_code, BADDATA)

    def test_03_user_not_created_wrong_email_format(self):

        token, index = authorization()
        time.sleep(3)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        self.command_user_create = 'management/users/create'
        self.url_user_create = '{}/{}'.format(HOST, self.command_user_create)
        words = ["python", "jumble", "easy", "difficult", "answer", "xylophone"]
        newvalue = random.choice(words) + random.choice(words)
        nameunique = "testuser" + random.choice(words)+ random.choice(words) + "@" + random.choice(words) + ".com"
        userdata = json.dumps({"full_name": newvalue, "email": "test", "password": "12345678", "password_confirmation": "12345678", "birthday": "1990-20-06"})

        response = self.s.post(self.url_user_create, data=userdata, headers=headers)

        self.assertEqual(response.status_code, BADDATA)


# PATCH /management/users/update/{id}
class Test_004_user_update(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_004_user_update, self).__init__(*a, **kw)
        self.s = requests.Session()

    def test_01_user_update_correctly(self):
        token, index = authorization()
        time.sleep(5)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        self.command_user_update = 'management/users/update'
        self.url_user_update = '{}/{}/{}'.format(HOST, self.command_user_update, index)
        userdata = json.dumps({"full_name": "User Updated", "birthday": "1990-10-20"})
        response = self.s.patch(self.url_user_update, data=userdata, headers=headers)
        updated_name = json.loads(response.content)['full_name']

        self.assertEqual(response.status_code, SUCCESS)
        self.assertEqual(updated_name, "User Updated")


# GET /management/users/search
#class Test_005_users_search(unittest.TestCase):
#
#    def __init__(self, *a, **kw):
#        super(Test_005_users_search, self).__init__(*a, **kw)
#        self.s = requests.Session()


# DELETE /management/users/delete/{id}
class Test_006_user_delete(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_006_user_delete, self).__init__(*a, **kw)
        self.s = requests.Session()

    def test_01_user_deleted_correctly(self):

        #Creating user before deleting
        self.command_signup = 'auth/signup'
        self.url_signup = '{}/{}'.format(HOST, self.command_signup)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        email_value = time.strftime("%d%m%Y" + "%H%M%S") + "@" + "test.com"
        userdata = json.dumps({"email": email_value, "full_name": "Test User"})
        response = self.s.post(self.url_signup, data=userdata, headers=headers)
        auth_token = response.headers['Authorization']
        user_id = json.loads(response.content)['id']

        self.command_user_delete = 'management/users/delete'
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': auth_token}
        self.url_user_delete = '{}/{}/{}'.format(HOST, self.command_user_delete, user_id)
        response = self.s.delete(self.url_user_delete, headers=headers)

        self.assertEqual(response.status_code, NO_CONTENT)


# POST /management/users/attach/role
class Test_007_Role_Attaching(unittest.TestCase):
    def __init__(self, *a, **kw):
        super(Test_007_Role_Attaching, self).__init__(*a, **kw)
        self.s = requests.Session()

    def test_01_role_is_attached_successfully(self):

        #get one role before attach
        token, user_id = authorization()
        time.sleep(3)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}

        self.command_get_role = 'management/roles'
        self.url_create_role = '{}/{}'.format(HOST, self.command_get_role)
        response = self.s.get(self.url_create_role, headers=headers)
        role_id = json.loads(response.content)['data'][1]['id']
        self.config = SafeConfigParser()
        self.config.read('config.ini')
        self.config.set('for_test', 'role_id', str(role_id))
        with open('config.ini', 'w') as f:
            self.config.write(f)

        self.assertEqual(response.status_code, SUCCESS)

        self.command_role_attach = 'management/users/attach/role'
        self.userId = 'userId'
        self.role_id = 'role_id'
        self.url_role_attach = '{}/{}?{}={}&{}={}'.format(HOST, self.command_role_attach,self.userId, user_id,
                                                          self.role_id, role_id)
        response = self.s.post(self.url_role_attach, headers=headers)

        self.assertEqual(response.status_code, NO_CONTENT)


# DELETE /management/users/detach/role
class Test_008_Role_Detaching(unittest.TestCase):
    def __init__(self, *a, **kw):
        super(Test_008_Role_Detaching, self).__init__(*a, **kw)
        self.s = requests.Session()
        self.config = SafeConfigParser()
        self.config.read('config.ini')

    def test_01_role_is_detached_successfully(self):

        token, user_id = authorization()
        time.sleep(3)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}

        role_id = self.config.getint('for_test', 'role_id')

        self.command_role_detach = 'management/users/detach/role'
        self.userId = 'userId'
        self.role_id = 'role_id'
        self.url_role_detach = '{}/{}?{}={}&{}={}'.format(HOST, self.command_role_detach, self.userId,
                                                                 user_id, self.role_id, role_id)
        response = self.s.delete(self.url_role_detach, headers=headers)

        self.assertEqual(response.status_code, NO_CONTENT)


                # --------------------- MANAGEMENT CATEGORIES --------------------------- #

# POST /management/categories/create
class Test_009_category_Creation(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_009_category_Creation, self).__init__(*a, **kw)
        self.s = requests.Session()

    def test_01_category_created_correctly(self):

        token, index = authorization()
        time.sleep(3)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        self.command_category_create = 'management/categories/create'
        self.url_category_create = '{}/{}'.format(HOST, self.command_category_create)
        userdata = json.dumps({"parent_id": 3, "title": "AutoTest", "description": "string"})
        response = self.s.post(self.url_category_create, data=userdata, headers=headers)
        title = json.loads(response.content)['title']

        self.assertEqual(response.status_code, SUCCESS)
        self.assertEqual(title, "AutoTest")


# GET /management/categories/search
#class Test_010_business_Creation(unittest.TestCase):
#
#    def __init__(self, *a, **kw):
#        super(Test_010_business_Creation, self).__init__(*a, **kw)
#        self.s = requests.Session()


# PATCH /management/categories/update/{id}
# DELETE /management/categories/delete/{id}
class Test_011_category_Update_And_Delete(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_011_category_Update_And_Delete, self).__init__(*a, **kw)
        self.s = requests.Session()
        self.token, self.index = authorization()

    def test_01_category_deleted_correctly(self):
        # Create before update and delete
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': self.token}
        self.command_category_create = 'management/categories/create'
        self.url_category_create = '{}/{}'.format(HOST, self.command_category_create)
        userdata = json.dumps({"parent_id": 2, "title": "forUpdate", "description": "string"})

        response = self.s.post(self.url_category_create, data=userdata, headers=headers)
        identifier = json.loads(response.content)['id']

        self.assertEqual(response.status_code, SUCCESS)

        self.command_category_update = 'management/categories/update'
        self.isocode = 'isocode1'
        self.isocode_value = 'en'
        self.url_category_update = '{}/{}/{}?{}={}'.format(HOST, self.command_category_update, identifier,
                                                               self.isocode, self.isocode_value)
        userdata = json.dumps({"title": "categoryTest"})
        response = self.s.patch(self.url_category_update, data=userdata, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)

        self.command_category_delete = 'management/categories/delete'
        self.url_category_delete = '{}/{}/{}'.format(HOST, self.command_category_delete, identifier)
        response = self.s.delete(self.url_category_delete, headers=headers)

        self.assertEqual(response.status_code, NO_CONTENT)

    def test_02_not_deleted_because_of_alphabetical_id(self):
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': self.token}
        self.command_category_delete = 'management/categories/delete'
        index = 'b'
        self.url_category_delete = '{}/{}/{}'.format(HOST, self.command_category_delete, index)
        response = self.s.delete(self.url_category_delete, headers=headers)

        self.assertEqual(response.status_code, WRONGID)

    def test_03_category_cant_be_deleted_because_id_doesnt_exist(self):
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': self.token}
        self.command_category_delete = 'management/categories/delete'
        index = 900
        self.url_category_delete = '{}/{}/{}'.format(HOST, self.command_category_delete, index)
        response = self.s.delete(self.url_category_delete, headers=headers)

        self.assertEqual(response.status_code, BADDATA)


# POST /management/categories/attach/tag
# DELETE /management/categories/detach/tag
class Test_012_Tag_Attaching_To_Category(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_012_Tag_Attaching_To_Category, self).__init__(*a, **kw)
        self.s = requests.Session()

    def test_01_attaching_tags_to_category(self):
        token, index = authorization()
        self.command_category_create = 'management/categories/create'
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        self.url_category_create = '{}/{}'.format(HOST, self.command_category_create)
        userdata = json.dumps({"parent_id": 3, "title": "string", "description": "string"})
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
        response = self.s.delete(self.url_tag_detaching_to_category, headers=headers)

        self.assertEqual(response.status_code, NO_CONTENT)

        self.command_category_delete = 'management/categories/delete'
        self.url_category_delete = '{}/{}/{}'.format(HOST, self.command_category_delete, index)
        response = self.s.delete(self.url_category_delete, headers=headers)

        self.assertEqual(response.status_code, NO_CONTENT)


             # --------------------- MANAGEMENT ROLE --------------------------- #

# GET /management/roles
class Test_013_Roles(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_013_Roles, self).__init__(*a, **kw)
        self.s = requests.Session()
        self.token, self.index = authorization()

    def test_01_role_show_correctly(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': self.token}
        self.command_get_all_roles = 'management/roles'
        self.url_get_all_roles = '{}/{}'.format(HOST, self.command_get_all_roles)
        response = self.s.get(self.url_get_all_roles, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)

class Test_014_ROLE_CRUD(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_014_ROLE_CRUD, self).__init__(*a, **kw)
        self.s = requests.Session()
        self.token, self.index = authorization()
        self.config = SafeConfigParser()

    def test_01_role_create(self):
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': self.token}
        self.command_create_roles = 'management/roles/create'
        self.url_create_roles = '{}/{}'.format(HOST, self.command_create_roles)
        roledata = json.dumps({"name": "AutoTest"})
        response = self.s.post(self.url_create_roles, data=roledata, headers=headers)
        dataresponse = json.loads(response.content)

        self.assertEqual(response.status_code, SUCCESS)
        self.assertEqual(dataresponse['name'], "AutoTest")

        self.config.read('config.ini')
        self.config.set('for_test', 'role_id_for_crud', str(dataresponse['id']))
        with open('config.ini', 'w') as f:
            self.config.write(f)

    def test_02_role_update(self):
        self.config.read('config.ini')
        role_id = self.config.getint('for_test', 'role_id_for_crud')
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': self.token}
        self.command_update_roles = 'management/roles/update'
        self.url_update_roles = '{}/{}/{}'.format(HOST, self.command_update_roles, role_id)
        roledata = json.dumps({"name": "AutoTestUpdate"})
        response = self.s.patch(self.url_update_roles, data=roledata, headers=headers)
        name = json.loads(response.content)['name']

        self.assertEqual(response.status_code, SUCCESS)
        self.assertEqual(name, "AutoTestUpdate")

    def test_03_role_show(self):
        self.config.read('config.ini')
        role_id = self.config.getint('for_test', 'role_id_for_crud')
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': self.token}
        self.command_update_roles = 'management/roles/show'
        self.url_update_roles = '{}/{}/{}'.format(HOST, self.command_update_roles, role_id)
        response = self.s.get(self.url_update_roles, headers=headers)
        name = json.loads(response.content)['name']

        self.assertEqual(response.status_code, SUCCESS)
        self.assertEqual(name, "AutoTestUpdate")

    def test_04_role_delete(self):
        self.config.read('config.ini')
        role_id = self.config.getint('for_test', 'role_id_for_crud')
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': self.token}
        self.command_delete_roles = 'management/roles/delete'
        self.url_delete_roles = '{}/{}/{}'.format(HOST, self.command_delete_roles, role_id)
        response = self.s.delete(self.url_delete_roles, headers=headers)

        self.assertEqual(response.status_code, NO_CONTENT)
        self.config.set('for_test', 'role_id_for_crud', '')
        with open('config.ini', 'w') as f:
            self.config.write(f)


            # --------------------- MANAGEMENT BUSINESS --------------------------- #


class Test_015_business_CRUD(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_015_business_CRUD, self).__init__(*a, **kw)
        self.s = requests.Session()
        self.token, self.index = authorization()
        self.config = SafeConfigParser()
        self.headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': self.token}

# POST /management/businesses/create
    def test_01_business_created_correctly(self):

        self.command_business_create = 'management/businesses/create'
        self.url_business_create = '{}/{}'.format(HOST, self.command_business_create)
        email_value = time.strftime("%d%m%Y" + "%H%M%S") + "@" + "test.com"
        userdata = json.dumps({"partner_id": 1, "email": email_value, "business_id_by_partner": "string",
                               "address": "testAddress", "geo_latitude": "48.92279", "geo_longitude": "22.4519749",
                               "name": "string", "description": "string"})
        response = self.s.post(self.url_business_create, data=userdata, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)

        business_id = json.loads(response.content)['id']
        self.config.read('config.ini')
        self.config.set('for_test', 'business_id_for_crud', str(business_id))
        with open('config.ini', 'w') as f:
            self.config.write(f)

    def test_02_business_not_created_because_empty_userdata(self):

        self.command_business_create = 'management/businesses/create'
        self.url_business_create = '{}/{}'.format(HOST, self.command_business_create)
        userdata = json.dumps({})
        response = self.s.post(self.url_business_create, data=userdata, headers=self.headers)

        self.assertEqual(response.status_code, BADDATA)

# PATCH /management/businesses/update
    def test_03_business_update_correctly(self):

        self.config.read('config.ini')
        business_id = self.config.getint('for_test', 'business_id_for_crud')
        self.command_business_update = 'management/businesses/update'
        self.url_business_update = '{}/{}/{}'.format(HOST, self.command_business_update, business_id)
        userdata = json.dumps({"name": "BusinessUpdate"})
        response = self.s.patch(self.url_business_update, data=userdata, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)
        title = json.loads(response.content)['name']
        self.assertEqual(title, "BusinessUpdate")

# GET /management/businesses/show
    def test_04_business_page_showed_correctly(self):

        self.config.read('config.ini')
        business_id = self.config.getint('for_test', 'business_id_for_crud')
        self.command_business_show = 'businesses/show'
        self.url_business_show = '{}/{}/{}'.format(HOST, self.command_business_show, business_id)
        response = self.s.get(self.url_business_show, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)
        self.assertEqual(json.loads(response.content)['id'], business_id)

# DELETE /management/businesses/delete
    def test_05_business_delete_correctly(self):

        self.config.read('config.ini')
        business_id = self.config.getint('for_test', 'business_id_for_crud')
        self.command_business_delete = 'management/businesses/delete'
        self.url_business_delete = '{}/{}/{}'.format(HOST, self.command_business_delete, business_id)
        response = self.s.delete(self.url_business_delete, headers=self.headers)

        self.assertEqual(response.status_code, NO_CONTENT)
        self.config.read('config.ini')
        self.config.set('for_test', 'business_id_for_crud', '')
        with open('config.ini', 'w') as f:
            self.config.write(f)


            # --------------------- MANAGEMENT PARTNERS --------------------------- #

# GET /management/partners
class Test_016_All_Partners(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_016_All_Partners, self).__init__(*a, **kw)
        self.s = requests.Session()

    def test_01_all_partners_opened(self):

        self.command_all_partners = 'management/partners'
        self.url_all_partners = '{}/{}'.format(HOST, self.command_all_partners)
        token, index = authorization()
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        response = self.s.get(self.url_all_partners, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)

# GET management/partners/show
class Test_017_Partner_Show(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_017_Partner_Show, self).__init__(*a, **kw)
        self.s = requests.Session()

    def test_01_partner_page_showed_correctly(self):

        token, index = authorization()
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        self.command_all_partners = 'management/partners'
        self.url_all_partners = '{}/{}'.format(HOST, self.command_all_partners)
        response = self.s.get(self.url_all_partners, headers=headers)
        partner = json.loads(response.content)['data'][0]

        self.command_partner_show = 'management/partners/show'
        self.url_partner_show = '{}/{}/{}'.format(HOST, self.command_partner_show, partner['id'])
        response = self.s.get(self.url_partner_show, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)
        self.assertEqual(json.loads(response.content), partner)


# class Test_018_Partner_Creation(unittest.TestCase):
#     def __init__(self, *a, **kw):
#         super(Test_018_Partner_Creation, self).__init__(*a, **kw)
#
#     def test_01_partner_created_correctly(self):
#         with open('USER_DATA.json') as data_file:
#             data = json.load(data_file)
#         s = requests.Session()
#         headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
#         self.host = host
#         self.command_partner_create = 'management/partners/create'
#
#         self.url_partner_create = 'http://{}/{}'.format(self.host, self.command_partner_create)
#         words = ["python", "jumble", "easy", "difficult", "answer", "xylophone"]
#         newvalue = random.choice(words) + random.choice(words)
#         nameunique = "testuser" + random.choice(words) + random.choice(words)
#         userdata = json.dumps({"name": newvalue, "sync_period": nameunique})
#
#         response2 = s.post(self.url_partner_create, data=userdata, headers=headers)
#
#         self.assertEqual(response2.status_code, SUCCESS)
#

class Test_019_Partner_Updating(unittest.TestCase):
        def __init__(self, *a, **kw):
            super(Test_019_Partner_Updating, self).__init__(*a, **kw)
            self.s = requests.Session()

        def test_01_partner_updated_correctly(self):

            token, index = authorization()
            time.sleep(3)
            headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
            index = 6
            self.command_partner_update = 'management/partners/update'
            self.url_partner_update = '{}/{}/{}'.format(HOST, self.command_partner_update, index)
            userdata = json.dumps({"sync_period": "daily"})
            response = self.s.patch(self.url_partner_update, data=userdata, headers=headers)

            self.assertEqual(response.status_code, SUCCESS)


            # --------------------- MANAGEMENT ACTIONS --------------------------- #

# GET /management/actions
class Test_020_ServerActions(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_020_ServerActions, self).__init__(*a, **kw)
        self.s = requests.Session()
        self.command_actions = 'management/actions'
        self.url_all_actions = '{}/{}'.format(HOST, self.command_actions)

    def test_01_all_actions_showed_successfully(self):

        token, index  = authorization()
        time.sleep(3)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        response = self.s.get(self.url_all_actions, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)


            # --------------------- MANAGEMENT OFFERS --------------------------- #

class Test_021_offer_CRUD(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_021_offer_CRUD, self).__init__(*a, **kw)
        self.s = requests.Session()
        self.token, self.index = authorization()
        self.config = SafeConfigParser()
        self.headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': self.token}

    def test_01_offer_created_correctly(self):

        self.command_category_create = 'management/categories/create'
        self.url_category_create = '{}/{}'.format(HOST, self.command_category_create)
        userdata = json.dumps({"parent_id": 3, "is_last": "false", "title": "ForOffer", "description": "string"})
        response = self.s.post(self.url_category_create, data=userdata, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)

        identifier = json.loads(response.content)['id']
        self.command_business_create = 'management/businesses/create'
        self.url_business_create = '{}/{}'.format(HOST, self.command_business_create)
        email_value = time.strftime("%d%m%Y" + "%H%M%S") + "@" + "test.com"
        userdata = json.dumps(
            {"partner_id": 1, "email": email_value, "business_id_by_partner": "string", "address": "string",
             "geo_latitude": "48.92279", "geo_longitude": "22.4519749", "name": "ForOffer", "description": "string"})
        response = self.s.post(self.url_business_create, data=userdata, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)

        index = json.loads(response.content)['id']

        self.command_offer_create = 'management/offers/create'
        self.url_offer_create = '{}/{}'.format(HOST, self.command_offer_create)
        userdata = json.dumps({"title": "OfferForTest", "description": "string", "business_id": index, "main_category_id": identifier, "SKU": "string","offer_quantity": 0, "offer_id_by_partner": "string", "delivery_cost": 0, "vat": 0})
        response = self.s.post(self.url_offer_create, data=userdata, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)

        offer_id = json.loads(response.content)['id']
        self.config.read('config.ini')
        self.config.set('for_test', 'offer_id_for_crud', str(offer_id))
        with open('config.ini', 'w') as f:
            self.config.write(f)

# PATCH /management/offers/update/{id}
    def test_02_offer_update_correctly(self):

        self.config.read('config.ini')
        offer_id = self.config.getint('for_test', 'offer_id_for_crud')
        self.command_business_update = 'management/offers/update'
        self.url_business_update = '{}/{}/{}'.format(HOST, self.command_business_update, offer_id)
        userdata = json.dumps({"title": "OfferUpdate"})
        response = self.s.patch(self.url_business_update, data=userdata, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)

        title = json.loads(response.content)['title']
        self.assertEqual(title, "OfferUpdate")

# GET /management/offers/show
    def test_03_offer_page_showed_correctly(self):

        self.config.read('config.ini')
        offer_id = self.config.getint('for_test', 'offer_id_for_crud')
        self.command_offer_show = 'offers/show'
        self.latitude = 'latitude=59.3258414'
        self.longitude = 'longitude=17.7073729'

        self.url_offer_show = '{}/{}/{}?{}&{}'.format(HOST, self.command_offer_show, offer_id, self.latitude, self.longitude)
        response = self.s.get(self.url_offer_show, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)
        self.assertEqual(json.loads(response.content)['id'], offer_id)

# POST /management/offers/approve
    def test_04_offer_approve(self):

        self.config.read('config.ini')
        offer_id = self.config.getint('for_test', 'offer_id_for_crud')
        self.command_offer_approve = 'management/offers/approve'
        self.parametr = 'offer_ids'

        self.url_offer_approve = '{}/{}?{}={}'.format(HOST, self.command_offer_approve, self.parametr, offer_id)
        response = self.s.post(self.url_offer_approve, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)
        status = json.loads(response.content)['data'][0]['status']
        self.assertEqual(status, 'approved')

# POST /management/offers/disapprove
    def test_05_offer_disapprove(self):

        self.config.read('config.ini')
        offer_id = self.config.getint('for_test', 'offer_id_for_crud')
        self.command_offer_disapprove = 'management/offers/disapprove'
        self.parametr = 'offer_ids'

        self.url_offer_disapprove = '{}/{}?{}={}'.format(HOST, self.command_offer_disapprove, self.parametr, offer_id)
        response = self.s.post(self.url_offer_disapprove, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)
        status = json.loads(response.content)['data'][0]['status']
        self.assertEqual(status, 'manual')

# POST /management/offers/publish
    def test_06_offer_publish(self):

        self.config.read('config.ini')
        offer_id = self.config.getint('for_test', 'offer_id_for_crud')
        self.command_offer_publish = 'management/offers/publish'
        self.parametr = 'offer_ids'

        self.url_offer_publish = '{}/{}?{}={}'.format(HOST, self.command_offer_publish, self.parametr, offer_id)
        response = self.s.post(self.url_offer_publish, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)
        status = json.loads(response.content)['data'][0]['status']
        self.assertEqual(status, 'published')

# POST /management/offers/unpublish
    def test_07_offer_unpublish(self):

        self.config.read('config.ini')
        offer_id = self.config.getint('for_test', 'offer_id_for_crud')
        self.command_offer_unpublish = 'management/offers/unpublish'
        self.parametr = 'offer_ids'

        self.url_offer_unpublish = '{}/{}?{}={}'.format(HOST, self.command_offer_unpublish, self.parametr, offer_id)
        response = self.s.post(self.url_offer_unpublish, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)
        status = json.loads(response.content)['data'][0]['status']
        self.assertEqual(status, 'approved')

# POST /management/offers/require-categorization
    def test_08_offer_requireCategorization(self):

        self.config.read('config.ini')
        offer_id = self.config.getint('for_test', 'offer_id_for_crud')
        self.command_offer_requireCategorization = 'management/offers/require-categorization'
        self.parametr = 'offer_ids'

        self.url_offer_requireCategorization = '{}/{}?{}={}'.format(HOST, self.command_offer_requireCategorization, self.parametr, offer_id)
        response = self.s.post(self.url_offer_requireCategorization, headers=self.headers)

        self.assertEqual(response.status_code, SUCCESS)
        status = json.loads(response.content)['data'][0]['categorization_required']
        self.assertEqual(status, True)

# DELETE /management/offers/delete
    def test_09_offer_delete_correctly(self):

        self.config.read('config.ini')
        offer_id = self.config.getint('for_test', 'offer_id_for_crud')
        self.command_offer_delete = 'management/offers/delete'
        self.url_offer_delete = '{}/{}/{}'.format(HOST, self.command_offer_delete, offer_id)
        response = self.s.delete(self.url_offer_delete, headers=self.headers)

        self.assertEqual(response.status_code, NO_CONTENT)

        self.config.read('config.ini')
        self.config.set('for_test', 'offer_id_for_crud', '')
        with open('config.ini', 'w') as f:
            self.config.write(f)



class Test_004_offer_Extra_Categories(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_004_offer_Extra_Categories, self).__init__(*a, **kw)
        self.s = requests.Session()

    def test_01_offer_added_and_removed_extra_categories_correctly(self):

        token, index = authorization()
        time.sleep(3)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        self.command_category_create = 'management/categories/create'
        self.url_category_create = '{}/{}'.format(HOST, self.command_category_create)
        userdata = json.dumps({"parent_id": 2, "title": "string", "description": "string"})
        response = self.s.post(self.url_category_create, data=userdata, headers=headers)
        identifier = json.loads(response.content)['id']

        self.assertEqual(response.status_code, SUCCESS)

        self.command_offer_create = 'management/offers/create'
        self.command_offer_attach_extra_category = 'management/offers/attach/extra-categories'
        self.command_offer_detach_extra_category = 'management/offers/detach/extra-categories'
        self.command_offer_delete = 'management/offers/delete'
        self.command_category_create = 'management/categories/create'

        self.url_category_create = '{}/{}'.format(HOST, self.command_category_create)
        userdata = json.dumps({"parent_id": 3, "is_last": "false", "title": "string", "description": "string"})
        response = self.s.post(self.url_category_create, data=userdata, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)

        identifier = json.loads(response.content)['id']
        self.command_business_create = 'management/businesses/create'
        self.url_business_create = '{}/{}'.format(HOST, self.command_business_create)
        email_value = time.strftime("%d%m%Y" + "%H%M%S") + "@" + "test.com"
        userdata = json.dumps(
            {"partner_id": 1, "email": email_value, "business_id_by_partner": "string", "address": "string",
             "geo_latitude": "48.92279", "geo_longitude": "22.4519749", "name": "string", "description": "string"})
        response = self.s.post(self.url_business_create, data=userdata, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)

        index = json.loads(response.content)['id']
        self.command_offer_create = 'management/offers/create'
        self.url_offer_create = '{}/{}'.format(HOST, self.command_offer_create)
        userdata = json.dumps(
            {"title": "string1", "description": "string", "business_id": index, "main_category_id": identifier,
             "SKU": "string", "offer_quantity": 0, "offer_id_by_partner": "string", "delivery_cost": 0, "vat": 0})
        response = self.s.post(self.url_offer_create, data=userdata, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)

        index = json.loads(response.content)['id']
        self.offer_ids = 'offer_id'
        self.category_ids = 'category_ids'
        self.url_offer_attach_extra_categories = '{}/{}?{}={}&{}={}'.format(HOST,
                                                                            self.command_offer_attach_extra_category,
                                                                            self.offer_ids, index, self.category_ids,
                                                                            identifier)
        response = self.s.post(self.url_offer_attach_extra_categories, headers=headers)

        self.assertEqual(response.status_code, NO_CONTENT)

        self.url_offer_detach_extra_categories = '{}/{}?{}={}&{}={}'.format(HOST,
                                                                            self.command_offer_detach_extra_category,
                                                                            self.offer_ids, index,
                                                                            self.category_ids, identifier)
        response = self.s.delete(self.url_offer_detach_extra_categories, headers=headers)

        self.assertEqual(response.status_code, NO_CONTENT)

        self.command_category_delete = 'management/categories/delete'
        self.url_category_delete = '{}/{}/{}'.format(HOST, self.command_category_delete, identifier)
        response = self.s.delete(self.url_category_delete, headers=headers)

        self.assertEqual(response.status_code, NO_CONTENT)

        self.command_offer_delete = 'management/offers/delete'
        self.url_offer_delete = '{}/{}/{}'.format(HOST, self.command_offer_delete, index)
        response = self.s.delete(self.url_offer_delete, headers=headers)

        self.assertEqual(response.status_code, NO_CONTENT)


class Test_004_Image_Attaching(unittest.TestCase):
    def __init__(self, *a, **kw):
        super(Test_004_Image_Attaching, self).__init__(*a, **kw)
        self.s = requests.Session()

    def test_01_image_is_attached_successfully(self):

        token, user_id = authorization()
        time.sleep(3)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        self.partner_id = 'partner_id'
        partner_id = 6
        self.image_id = 'image_id'
        image_id = 612

        self.command_image_attach = 'management/partners/image/attach'
        self.command_image_detach = 'management/partners/image/detach'
        self.url_image_attach = '{}/{}?{}={}&{}={}'.format(HOST, self.command_image_attach, self.partner_id,
                                                                 partner_id, self.image_id, image_id)
        response = self.s.post(self.url_image_attach, headers=headers)

        self.assertEqual(response.status_code, ADDED)
        self.url_image_detach = '{}/{}?{}={}&{}={}'.format(HOST, self.command_image_detach, self.partner_id,
                                                                 partner_id, self.image_id, image_id)
        response = self.s.delete(self.url_image_detach, headers=headers)

        self.assertEqual(response.status_code, FINISHED)


class Test_004_attach_image_to_business(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_004_attach_image_to_business, self).__init__(*a, **kw)
        self.s = requests.Session()

    def test_01_image_is_attached_successfully(self):

        token, index = authorization()
        time.sleep(5)
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': token}
        self.command_business_create = 'management/businesses/create'

        self.url_business_create = '{}/{}'.format(HOST, self.command_business_create)
        email_value = time.strftime("%d%m%Y" + "%H%M%S") + "@" + "test.com"
        userdata = json.dumps \
            ({"partner_id": 1, "email": email_value, "business_id_by_partner": "string", "address": "string", "geo_latitude": "48.92279", "geo_longitude": "22.4519749", "name": "string", "description": "string"})
        response = self.s.post(self.url_business_create, data=userdata, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)

        identificator = json.loads(response.content)['id']
        self.command_businesses_image_attach = 'management/businesses/image/attach'
        self.command_businesses_image_detach = 'management/businesses/image/detach'

        self.business_id = 'business_id'
        self.image_id = 'image_id'
        image_id = 612
        self.url_businesses_image_attach = '{}/{}?{}={}&{}={}'.format(HOST, self.command_businesses_image_attach, self.business_id,
                                                                  identificator, self.image_id, image_id)
        response = self.s.post(self.url_businesses_image_attach, headers=headers)

        self.assertEqual(response.status_code, ADDED)

        self.url_businesses_image_detach = '{}/{}?{}={}&{}={}'.format(HOST,
                                                                             self.command_businesses_image_detach,
                                                                             self.business_id,
                                                                             identificator, self.image_id, image_id)
        response = self.s.delete(self.url_businesses_image_detach, headers=headers)

        self.assertEqual(response.status_code, FINISHED)

        self.command_business_delete = 'management/businesses/delete'
        self.url_business_delete = '{}/{}/{}'.format(HOST, self.command_business_delete, identificator)
        response = self.s.delete(self.url_business_delete, headers=headers)

        self.assertEqual(response.status_code, NO_CONTENT)


class Test_004_Image_Uploading(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_004_Image_Uploading, self).__init__(*a, **kw)
        self.s = requests.Session()

    def test_01_image_is_upload_successfully(self):

        token, user_id = authorization()
        time.sleep(3)
        headers = {'Authorization': token}
        self.partner_id = 'partner_id'
        self.image_id = 'image_id'
        self.command_image_upload = 'management/images/upload'
        self.url_image_upload = '{}/{}'.format(HOST, self.command_image_upload)
        postdata = {}
        files = {'image': open('picture.jpg', 'rb')}
        response = self.s.post(self.url_image_upload, headers=headers, data=postdata, files=files )
        identificator = json.loads(response.content)['id']

        self.assertEqual(response.status_code, SUCCESS)

        self.command_image_delete = 'management/images/delete'
        self.url_image_delete = '{}/{}/{}'.format(HOST, self.command_image_delete, identificator)
        response = self.s.delete(self.url_image_delete, headers=headers)

        self.assertEqual(response.status_code, NO_CONTENT)


if __name__ == '__main__':
    unittest.main()
