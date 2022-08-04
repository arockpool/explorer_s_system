import time
import json
import logging
from collections import Iterable

from django.http import HttpResponse

from explorer_s_common.page import Page
from explorer_s_common.decorator import common_ajax_response
from explorer_s_common.utils import format_return, format_price
from explorer_s_common import inner_server

from notice.interface import NoticeBase, FaqBase


def format_notice(objs):
    if objs is None:
        return None

    def _format_obj(obj):
        return {
            'id': obj.id, 'category': obj.category, 'category_str': obj.get_category_display(),
            'title': obj.title, 'content': obj.content, 'state': obj.state,
            'state_str': obj.get_state_display(), 'author': obj.author,
            'publish_time': obj.publish_time.strftime('%Y-%m-%d %H:%M:%S'),
            'create_time': obj.create_time.strftime('%Y-%m-%d %H:%M:%S')
        }

    return [_format_obj(obj) for obj in objs] if isinstance(objs, Iterable) else _format_obj(objs)


@common_ajax_response
def get_notice_list(request):
    page_index = int(request.POST.get('page_index', 1))
    page_count = min(int(request.POST.get('page_count', 10)), 50)

    objs = NoticeBase().get_notice(state=1)
    data = Page(objs, page_count).page(page_index)

    return format_return(0, data={
        'objs': format_notice(data['objects']), 'total_page': data['total_page'], 'total_count': data['total_count']
    })


@common_ajax_response
def get_notice_by_id(request):
    obj_id = request.POST.get('obj_id')
    obj = NoticeBase().get_notice_by_id(obj_id=obj_id)

    return format_return(0, data=format_notice(obj))


def format_faq(objs):
    if objs is None:
        return None

    def _format_obj(obj):
        return {
            'id': obj.id, 'sort': obj.sort, 'title': obj.title,
            'content': obj.content, 'state': obj.state, 'state_str': obj.get_state_display(),
            'create_time': obj.create_time.strftime('%Y-%m-%d %H:%M:%S')
        }

    return [_format_obj(obj) for obj in objs] if isinstance(objs, Iterable) else _format_obj(objs)


@common_ajax_response
def get_faq_list(request):
    page_index = int(request.POST.get('page_index', 1))
    page_count = min(int(request.POST.get('page_count', 10)), 50)

    objs = FaqBase().get_faq(state=1)
    data = Page(objs, page_count).page(page_index)

    return format_return(0, data={
        'objs': format_faq(data['objects']), 'total_page': data['total_page'], 'total_count': data['total_count']
    })


@common_ajax_response
def get_faq_by_id(request):
    obj_id = request.POST.get('obj_id')
    obj = FaqBase().get_faq_by_id(obj_id=obj_id)

    return format_return(0, data=format_faq(obj))


@common_ajax_response
def get_notice_data_overview(request):
    result_dict = dict()
    overview_dict = inner_server.get_net_ovewview().get('data')  # 扇区质押,单币美元价格
    rate = inner_server.get_usd_rate().get("data")
    result_dict['avg_pledge'] = round(float(overview_dict['avg_pledge']) * 32, 4)
    result_dict['price'] = float(overview_dict['price'])
    result_dict['rmb'] = result_dict['price'] * float(rate)
    result_dict['rate'] = rate
    return format_return(0, data=result_dict)
