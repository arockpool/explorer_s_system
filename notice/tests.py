import datetime

from django.test import TestCase
from django.test.client import Client

from explorer_s_common.cache import Cache
from explorer_s_common import inner_server

from notice.interface import NoticeBase


class NoticeTestCase(TestCase):

    def setUp(self):
        self.client = Client(HTTP_USERID="1", HTTP_APPID='h5')

    def test_notice(self):
        result = self.client.post(
            '/system/admin/notice/add_notice', {
                'title': 'title11', 'content': 'content22'
            }
        ).json()
        print(result)

        result = self.client.post(
            '/system/api/notice/get_notice_list', {}
        ).json()
        print(result)
        obj_id = result['data']['objs'][0]['id']

        result = self.client.post(
            '/system/api/notice/get_notice_by_id', {'obj_id': obj_id}
        ).json()
        print(result)

        result = self.client.post(
            '/system/admin/notice/search_notice', {}
        ).json()
        print(result)

    def test_faq(self):
        result = self.client.post(
            '/system/admin/notice/add_faq', {
                'title': 'title11aa', 'content': 'content22'
            }
        ).json()
        print(result)

        result = self.client.post(
            '/system/api/notice/get_faq_list', {}
        ).json()
        print(result)
        obj_id = result['data']['objs'][0]['id']

        result = self.client.post(
            '/system/api/notice/get_faq_by_id', {'obj_id': obj_id}
        ).json()
        print(result)

        result = self.client.post(
            '/system/admin/notice/search_faq', {}
        ).json()
        print(result)
