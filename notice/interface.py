import datetime
import decimal
import os

import requests

from explorer_s_common.inner_server import get_calculate_info
from explorer_s_common import debug, consts, raw_sql, cache
from explorer_s_common.utils import format_return, Validator
from explorer_s_common.decorator import validate_params, cache_required

from explorer_s_system.consts import ERROR_DICT
from notice.models import Notice, Faq


class NoticeBase(object):

    def get_notice_by_id(self, obj_id):
        objs = Notice.objects.filter(id=obj_id)
        return objs[0] if objs else None

    def get_notice(self, state=None):
        objs = Notice.objects.filter()
        if state is not None:
            objs = objs.filter(state=state)
        return objs

    @validate_params
    def add_notice(self, publish_time, title, content=None, category=0, author=None, sort=0, state=0):
        obj = Notice.objects.create(
            title=title, content=content, category=category,
            publish_time=publish_time, author=author, sort=sort, state=state
        )
        return format_return(0, data={'obj_id': obj.id})

    @validate_params
    def modify_notice(self, obj_id, publish_time, title, content=None, category=0, author=None, sort=0, state=None):
        obj = self.get_notice_by_id(obj_id=obj_id)
        if not obj:
            return format_return(13000)

        obj.title = title
        obj.content = content
        obj.publish_time = publish_time
        obj.author = author
        obj.publish_time = publish_time
        obj.state = state
        obj.sort = sort
        obj.save()
        return format_return(0)

    def search_for_admin(self, title=None, state=None):
        objs = Notice.objects.filter()
        if title:
            objs = objs.filter(title__icontains=title)
        if state:
            objs = objs.filter(state=state)
        return objs

    def get_notice_data_overview(self):
        template = "当前FIL价格：1 FIL={} USDT ={} 元，矿池24h平均挖矿收益为 {}FIL/TiB，单T扇区质押为{}FIL/TiB"
        result = get_calculate_info()
        if result or result['code'] == 0:
            result_data = result['data']
            result_data["rmb_price"] = round(
                decimal.Decimal(result_data['rate']) * decimal.Decimal(result_data['price']), 2)
            return result_data

    def get_total_power(self):

        url = os.getenv('SERVER_ACTIVITY') + '/activity/api/dashboard/v2/get_pool_overview'
        result = requests.post(url=url, data={}, timeout=30)
        try:
            return result.json()
        except Exception as e:
            return {
                "total_power": 0
            }

    @staticmethod
    @cache_required(cache_key='mean_mining_earnings', expire=60 * 30)
    def mean_mining_earnings():
        # result = MiningEfficiency.objects.all().aggregate(efficiency=Avg('efficiency'))['efficiency']
        # result = format_fil_to_decimal(result) if result else 0
        # return result

        # 获取矿池挖矿效率
        url = 'https://api.rmdine.com/open/stat/solomine/data'
        try:
            pool_efficiency = requests.get(url, timeout=5).json()['data']
        except Exception as e:
            pool_efficiency = '0.1406'
        return pool_efficiency


class FaqBase(object):

    def get_faq_by_id(self, obj_id):
        objs = Faq.objects.filter(id=obj_id)
        return objs[0] if objs else None

    def get_faq(self, state=None):
        objs = Faq.objects.filter()
        if state is not None:
            objs = objs.filter(state=state)
        return objs

    @validate_params
    def add_faq(self, title, content=None, sort=0):
        obj = Faq.objects.create(title=title, content=content, sort=sort)
        return format_return(0, data={'obj_id': obj.id})

    @validate_params
    def modify_faq(self, obj_id, title, content=None, sort=0, state=1):
        obj = self.get_faq_by_id(obj_id=obj_id)
        if not obj:
            return format_return(13000)

        obj.title = title
        obj.content = content
        obj.sort = sort
        obj.state = state
        obj.save()
        return format_return(0)

    def search_for_admin(self, **kwargs):
        objs = Faq.objects.filter(**kwargs).order_by("-create_time")
        return objs
