import json
import requests
import unittest
import time

from authorization import test_authorization
from baseSettings import *


class Test_001_All_offers(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_001_All_offers, self).__init__(*a, **kw)
        self.command_all_offers = 'offers'
        self.command_get_offers = 'offers/get'
        self.isocode = 'isocode1'
        self.isocode_value = 'sv'
        self.latitude = 'latitude'
        latitude_value = 59.3258414
        self.longitude = 'longitude'
        longitude_value = 17.7073729
        self.page = 'page=1'
        self.limit = 'limit10'
        self.url_all_offers = '{}/{}?{}={}&{}={}&{}={}'.format(HOST, self.command_all_offers, self.isocode,
                                                               self.isocode_value, self.latitude, latitude_value,
                                                               self.longitude, longitude_value)
        self.url_get_offers = '{}/{}?{}&{}'.format(HOST, self.command_get_offers, self.page, self.limit)
        self.s = requests.Session()

    def test_01_all_offers_opened(self):
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        response = self.s.get(self.url_all_offers, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)

    def test_02_get_offers(self):
        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        response = self.s.get(self.url_get_offers, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)

class Test_002_offer_Show(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_002_offer_Show, self).__init__(*a, **kw)
        self.s = requests.Session()

    def test_01_offer_page_showed_correctly(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        self.command_all_offers = 'offers'
        self.isocode = 'isocode1'
        self.isocode_value = 'sv'
        self.latitude = 'latitude'
        latitude_value  = 59.3258414
        self.longitude = 'longitude'
        longitude_value = 17.7073729

        self.url_all_offers = '{}/{}?{}={}&{}={}&{}={}'.format(HOST, self.command_all_offers, self.isocode, self.isocode_value, self.latitude, latitude_value, self.longitude, longitude_value)
        offers = self.s.get(self.url_all_offers, headers=headers)
        m = json.loads(offers.content)
        index = int(m['data'][1]['id'])

        self.command_offer_show = 'offers/show'
        self.url_offer_show = '{}/{}/{}?{}={}&{}={}&{}={}'.format(HOST, self.command_offer_show, index, self.isocode, self.isocode_value, self.latitude, latitude_value, self.longitude, longitude_value)
        response = self.s.get(self.url_offer_show, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)


class Test_003_bestOffers(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_003_bestOffers, self).__init__(*a, **kw)
        self.s = requests.Session()

    def test_01_best_offers_showed_correctly(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER}
        self.command_best_offers = 'offers/best'
        self.isocode = 'isocode1'
        self.isocode_value = 'sv'
        self.category_ids_title = 'category_ids'
        self.category_ids_numbers = '85%2C86%2C87'
        self.sort_by = 'sort_by'
        sort_by_value = 'price'
        self.latitude = 'latitude'
        latitude_value = '59.3258414'
        self.longitude = 'longitude'
        longitude_value = '17.7073729'
        self.url_best_offers = '{}/{}?{}={}&{}={}&{}={}&{}={}&{}={}'.format(HOST, self.command_best_offers,
                                                                            self.isocode, self.isocode_value,
                                                                            self.category_ids_title,
                                                                            self.category_ids_numbers,self.latitude,
                                                                            latitude_value, self.longitude,
                                                                            longitude_value, self.sort_by, sort_by_value)
        response = self.s.get(self.url_best_offers, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)


class Test_004_offer_liking_disliking(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(Test_004_offer_liking_disliking, self).__init__(*a, **kw)
        self.token, self.index = test_authorization()
        self.s = requests.Session()

    def test_01_offer_liked_and_disliked_correctly(self):

        headers = {'content-type': DEFAULT_HEADER, 'accept': DEFAULT_HEADER, 'Authorization': self.token}
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

        identificator = json.loads(response.content)['id']

        self.offer_id = 'offer_id'

        self.command_offer_like = 'offers/like'
        self.url_offer_like = '{}/{}?{}={}'.format(HOST, self.command_offer_like, self.offer_id, identificator)
        response = self.s.post(self.url_offer_like, headers=headers)

        self.assertEqual(response.status_code, FINISHED)

        self.command_offer_dislike = 'offers/dislike'
        self.url_offer_dislike = '{}/{}?{}={}'.format(HOST, self.command_offer_dislike, self.offer_id,
                                                          identificator)
        response = self.s.post(self.url_offer_dislike, headers=headers)

        self.assertEqual(response.status_code, FINISHED)

        self.command_offer_delete = 'management/offers/delete'
        self.url_offer_delete = '{}/{}/{}'.format(HOST, self.command_offer_delete, identificator)
        response = self.s.delete(self.url_offer_delete, headers=headers)

        self.assertEqual(response.status_code, SUCCESS)


if __name__ == '__main__':
    unittest.main()
