import json
import datetime
import string
import uuid
import random
import yagmail

from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider
from aliyunsdksts.request.v20150401 import AssumeRoleRequest

from explorer_s_common import debug, consts, cache
from explorer_s_common.utils import format_return, Validator
from explorer_s_common.decorator import validate_params, cache_required
from explorer_s_common.third.welink_sdk import WeLinkBase

from explorer_s_system.consts import ERROR_DICT
from system.models import Admin, Appinfo


class OssBase(object):

    def get_oss_sts(self):
        '''
        获取阿里云oss授权凭证
        '''

        region_provider.add_endpoint('Sts', consts.OSS_STS_REGIONID, consts.OSS_STS_ENDPOINT)
        clt = client.AcsClient(consts.OSS_ACCESS_KEY_ID, consts.OSS_ACCESS_KEY_SECRET, consts.OSS_STS_REGIONID)
        request = AssumeRoleRequest.AssumeRoleRequest()
        request.set_RoleArn(consts.OSS_ROLE_ARN)
        request.set_RoleSessionName(consts.OSS_SESSION_NAME)
        response = clt.do_action_with_exception(request)
        token = json.loads(response.decode('utf-8'))
        return token


class EmailBase():

    @validate_params
    def send_email(self, emails, title, content=None):
        if not isinstance(emails, (list, tuple)):
            emails = [emails, ]

        for email in emails:
            if not Validator().validate_email(email):
                return format_return(99902)

        yag = yagmail.SMTP(
            # user={consts.EMAIL_SENDER: consts.EMAIL_SENDER_NICK},
            user=consts.EMAIL_SENDER,
            password=consts.EMAIL_SENDER_PASSWORD,
            host=consts.EMAIL_HOST, port=consts.EMAIL_PORT
        )
        yag.send(to=emails, subject=title, contents=content)
        return format_return(0)


class AdminBase(object):

    @validate_params
    def add_admin(self, user_id, permissions="", is_super=0):
        obj, created = Admin.objects.get_or_create(user_id=user_id)
        obj.permissions = permissions
        obj.is_super = is_super
        obj.save()
        return format_return(0, data={'obj_id': obj.id})

    def get_admin_by_user_id(self, user_id):
        '''
        获取用户的权限详情
        '''
        objs = Admin.objects.filter(user_id=user_id)
        return objs[0] if objs else None

    def get_admins(self):
        '''
        获取所有普通管理员
        '''
        return Admin.objects.filter(is_super=0)

    @staticmethod
    def get_common_admins():
        '''
        获取所有管理员
        '''
        return Admin.objects.all()

    @staticmethod
    def get_super_admins():
        '''
        获取所有超级管理员
        '''
        return Admin.objects.filter(is_super=1)

    def modify_admin_permissions(self, user_id, permissions):
        '''
        修改用户权限
        '''
        Admin.objects.filter(user_id=user_id).update(permissions=permissions)
        return format_return(0)

    def remove_admin(self, user_id):
        '''
        修改用户权限
        '''
        Admin.objects.filter(user_id=user_id).delete()
        return format_return(0)


class AppinfoBase(object):
    @classmethod
    def add_app_info(cls, user_id, remarks):
        app_id = ''.join(random.sample(string.ascii_lowercase + string.digits, 16))
        app_secret = uuid.uuid1().hex
        if not Appinfo.objects.filter(app_id=app_id).exists():
            Appinfo(app_id=app_id, app_secret=app_secret, opt_user_id=user_id, remarks=remarks).save()
            return app_id

    @classmethod
    def update_app_info(cls, app_id, user_id, is_app_secret=0, remarks=None,status=None):
        if Appinfo.objects.filter(app_id=app_id).exists():
            updates = dict(opt_user_id=user_id)
            if remarks:
                updates["remarks"] = remarks
            if is_app_secret:
                updates["app_secret"] = uuid.uuid1().hex
            if status:
                updates["status"] = status
            return Appinfo.objects.filter(app_id=app_id).update(**updates)

    @classmethod
    def get_app_infos(cls):
        '''
        获取所有
        '''
        return Appinfo.objects.all()

    @classmethod
    def get_app_info(cls, app_id):
        '''
        获取
        '''
        return Appinfo.objects.filter(app_id=app_id, status=1).first()

    @classmethod
    def del_app_info(cls, app_id, user_id):
        '''
        获取
        '''
        return Appinfo.objects.filter(app_id=app_id).update(status=False, opt_user_id=user_id)
