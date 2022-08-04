import os
import datetime
import requests

from explorer_s_common import debug, consts, cache
from explorer_s_common.utils import format_return, Validator
from explorer_s_common.decorator import validate_params, cache_required

from explorer_s_system.consts import ERROR_DICT
from monitor.models import SlowRequest, SysError, RequestLog


class SlowRequestBase(object):
    '''
    慢请求
    '''

    def __init__(self):
        self.validator = Validator()

    @validate_params
    def add_slow_request(self, url, duration, ip, post_data):
        # 添加慢请求

        today = datetime.datetime.now().date()
        if SlowRequest.objects.filter(record_date=today, url=url).count() >= 100:
            return format_return(15000)

        sr = SlowRequest.objects.create(url=url, duration=duration, ip=ip, post_data=post_data, record_date=today)
        return format_return(0, data=dict(id=sr.id))

    def get_slow_request(self, start_date=None, end_date=None, url=None):
        ps = {}
        if start_date:
            if not (self.validator.validate_date(start_date) and self.validator.validate_date(end_date)):
                return []
            ps.update(dict(record_date__gte=start_date, record_date__lt=end_date))
        if url:
            ps.update(dict(url=url))
        return SlowRequest.objects.filter(**ps)


class SysErrorBase(object):
    '''
    系统错误
    '''

    def __init__(self):
        self.validator = Validator()

    def send_email_notice(self, title, content):
        from system.interface import EmailBase
        EmailBase().send_email(emails=consts.EMAIL_NOTICE_GROUP, title=title, content=content)

    @validate_params
    def add_sys_error(self, service, url, detail):
        # 添加错误日志

        today = datetime.datetime.now().date()
        if SysError.objects.filter(url=url, record_date=today).count() >= 100:
            return format_return(15000)

        se = SysError.objects.create(service=service, url=url, detail=detail, record_date=today)
        if os.getenv('DEVCODE') == 'prod':
            self.send_email_notice(title=url, content=detail)
        return format_return(0, data=dict(id=se.id))

    def get_sys_error(self, start_date=None, end_date=None, url=None):
        ps = {}
        if start_date:
            if not (self.validator.validate_date(start_date) and self.validator.validate_date(end_date)):
                return []
            ps.update(dict(record_date__gte=start_date, record_date__lt=end_date))
        if url:
            ps.update(dict(url=url))
        return SysError.objects.filter(**ps)


class RequestLogBase(object):
    '''
    访问日志
    '''

    def add_request_log(self, url, post_data, res_data, request_time, duration,
                        app_id=None, ip=None):

        obj = RequestLog.objects.create(
            url=url, post_data=post_data, res_data=res_data,
            request_time=request_time, duration=duration, app_id=app_id, ip=ip
        )
        return format_return(0, data={'obj_id': obj.id})
