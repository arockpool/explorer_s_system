import json

from django.test import TestCase
from django.test.client import Client

from system.interface import AdminBase


class SystemTestCase(TestCase):

    def setUp(self):
        self.user_id = '1'
        self.client = Client(HTTP_USERID=self.user_id)

    def test_get_oss_sts(self):
        result = self.client.post(
            '/system/api/get_oss_sts', {}
        ).json()
        print(result)

    def test_permission(self):

        # 查询管理员权限
        result = self.client.post(
            '/system/admin/get_admin_permissions', {'user_id': self.user_id}
        ).json()
        print(result)

        # 添加管理员
        result = self.client.post(
            '/system/admin/add_admin', {
                'user_id': self.user_id,
                'permissions': json.dumps(["user_manage"])
            }
        ).json()
        print(result)

        # 查询管理员权限
        result = self.client.post(
            '/system/admin/get_admin_permissions', {'user_id': self.user_id}
        ).json()
        print(result)

        # 修改管理员权限
        result = self.client.post(
            '/system/admin/modify_admin_permissions', {
                'user_id': self.user_id,
                'permissions': json.dumps(['user_manage', 'coupon_manage'])
            }
        ).json()
        print(result)

        # 查询管理员权限
        result = self.client.post(
            '/system/admin/get_admin_permissions', {'user_id': self.user_id}
        ).json()
        print(result)

        # 查询管理员列表
        result = self.client.post(
            '/system/admin/get_admins', {}
        ).json()
        print(result)

        # 查询管理员列表
        result = self.client.post(
            '/system/admin/remove_admin', {'user_id': self.user_id}
        ).json()
        print(result)

    def test_send_sms(self):
        result = self.client.post(
            '/system/api/send_sms', {'mobile': '13488985003', 'content': '验证码123456，欢迎注册/登录一石云池，请勿泄露短信验证码。【一石云池】'}
        ).json()
        print(result)
