import json
import datetime
import decimal

from collections import Iterable

from explorer_s_common import inner_server, consts
from explorer_s_common.weixin.config import DICT_WEIXIN_APP
from explorer_s_common.weixin.interface import WeixinBase
from explorer_s_common.cache import Cache
from explorer_s_common.decorator import common_ajax_response
from explorer_s_common.utils import format_return
from explorer_s_common.third.welink_sdk import WeLinkBase
from system.serializer import AppinfoSerializer
from system.interface import OssBase, EmailBase, AppinfoBase


@common_ajax_response
def get_oss_sts(request):
    '''
    获取oss授权信息
    '''
    sts = OssBase().get_oss_sts()

    sts['Credentials']['bucket_name'] = consts.OSS_BUCKET_NAME
    sts['Credentials']['oss_regionid'] = consts.OSS_REGIONID
    sts['Credentials']['img_domain'] = consts.IMG_DOMAIN
    sts['Credentials']['oss_endpoint'] = consts.OSS_ENDPOINT
    return format_return(0, data=sts)


@common_ajax_response
def send_sms(request):
    '''
    发送短信
    '''
    mobile = request.POST.get('mobile')
    product_id = request.POST.get('product_id', "1012818")
    content = request.POST.get('content')
    is_hard = json.loads(request.POST.get('is_hard', '0'))
    sms_system = request.POST.dict()
    sms_system['product_id'] = product_id
    return WeLinkBase(init_dict=sms_system).send_sms(phone_no=mobile, content=content, is_hard=is_hard,
                                                     product_id=product_id)


@common_ajax_response
def send_email(request):
    '''
    发送邮件
    '''
    emails = request.POST.get('emails', consts.EMAIL_NOTICE_GROUP)
    title = request.POST.get('title')
    content = request.POST.get('content')
    return EmailBase().send_email(emails=emails, title=title, content=content)


@common_ajax_response
def auth_by_code(request):
    '''
    根据code换openid、unionid等信息
    '''
    config = DICT_WEIXIN_APP.get(request.app_id, {})
    if not config:
        return format_return(13001)

    wx_base = WeixinBase(
        app_id=config['app_id'], app_secret=config['app_secret'], origin_id=config['origin_id']
    )

    code = request.POST.get('code')
    open_id, session_key, union_id = wx_base.get_session_key(code=code)
    return format_return(0, data={'open_id': open_id, 'union_id': union_id})


@common_ajax_response
def decrypt_data(request):
    '''
    解密微信数据
    '''
    config = DICT_WEIXIN_APP.get(request.app_id, {})
    if not config:
        return format_return(13001)

    wx_base = WeixinBase(
        app_id=config['app_id'], app_secret=config['app_secret'], origin_id=config['origin_id']
    )

    open_id = request.POST.get('open_id')
    encrypted_data = request.POST.get('encrypted_data')
    iv = request.POST.get('iv')

    result = wx_base.decrypt_data(open_id, encrypted_data, iv)
    return format_return(0, data=result)


@common_ajax_response
def save_form_id(request):
    '''
    保存微信form_id 用于发送小程序通知
    '''
    config = DICT_WEIXIN_APP.get(request.app_id, {})
    if not config:
        return format_return(13001)

    wx_base = WeixinBase(
        app_id=config['app_id'], app_secret=config['app_secret'], origin_id=config['origin_id']
    )

    user_id = request.POST.get('user_id')
    form_id = request.POST.get('form_id')

    wx_base.save_form_id(user_id=user_id, form_id=form_id)
    return format_return(0)


@common_ajax_response
def get_access_token(request):
    '''
    获取访问token
    '''
    config = DICT_WEIXIN_APP.get(request.app_id, {})
    if not config:
        return format_return(13001)

    wx_base = WeixinBase(
        app_id=config['app_id'], app_secret=config['app_secret'], origin_id=config['origin_id']
    )

    access_token = wx_base.get_weixin_access_token()
    return format_return(0, data=access_token)


@common_ajax_response
def get_app_info(request):
    '''
    根据app_id
    '''
    app_id = request.POST.get('app_id')
    AppinfoBase.get_app_info(app_id)
    data = AppinfoSerializer(AppinfoBase.get_app_info(app_id)).data
    return format_return(0, data=data)
