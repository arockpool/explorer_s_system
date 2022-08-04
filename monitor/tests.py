import json
import datetime

from django.test import TestCase
from django.test.client import Client

from explorer_s_common.cache import Cache
from explorer_s_common import inner_server

from monitor.interface import SlowRequestBase, SysErrorBase


class MonitorTestCase(TestCase):

    def setUp(self):
        self.client = Client(HTTP_USERID='1')

    def log(self, msg):
        print()
        print('===== ' + msg + ' =====')

    def test_slow_request_api(self):
        '''
        '''
        url = '/a/1'
        start_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')

        self.log('添加记录')
        result = self.client.post(
            '/system/api/monitor/add_slow_request', {
                'url': url, 'duration': 1, 'ip': '128.0.0.1', 'post_data': 'aaa'
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 0)

        self.log('分组查询')
        result = self.client.post(
            '/system/api/monitor/get_slow_request_group', {
                'start_date': start_date,
                'end_date': end_date
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 0)

        self.log('单个查询')
        result = self.client.post(
            '/system/api/monitor/get_slow_request', {
                'start_date': start_date,
                'end_date': end_date,
                'url': url
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 0)

        self.log('inner_server调用')
        result = inner_server.add_slow_request(request_url=url, duration=1, ip='127.0.0.1', post_data='bbccbbdd')
        print(result)
        self.assertEqual(result['code'], 0)

    def test_sys_error_api(self):
        '''
        '''
        url = '/a/2'
        service = 'account'
        detail = '账号错误'
        start_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')

        self.log('添加记录')
        result = self.client.post(
            '/system/api/monitor/add_sys_error', {
                'url': url, 'service': service, 'detail': detail
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 0)

        self.log('分组查询')
        result = self.client.post(
            '/system/api/monitor/get_sys_error_group', {
                'start_date': start_date,
                'end_date': end_date
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 0)

        self.log('单个查询')
        result = self.client.post(
            '/system/api/monitor/get_sys_error', {
                'start_date': start_date,
                'end_date': end_date,
                'url': url
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 0)

        self.log('inner_server调用')
        result = inner_server.add_sys_error(service=service, request_url=url, detail=detail)
        print(result)
        self.assertEqual(result['code'], 0)

    def test_add_request_log(self):
        url = '/test/1'
        post_data = 'a=1'
        res_data = 'a'
        request_time = '2020-06-06 12:12:12'
        duration = '1'
        app_id = '12345'
        ip = '127.0.0.1'

        result = self.client.post(
            '/system/api/monitor/add_request_log', {
                'url': url, 'post_data': post_data, 'res_data': res_data, 'ip': ip,
                'request_time': request_time, 'duration': duration, 'app_id': app_id
            }
        ).json()
        print(result)
