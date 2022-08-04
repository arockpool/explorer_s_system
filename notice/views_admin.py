import time
import json
import logging
import datetime
from collections import Iterable

from django.http import HttpResponse

from explorer_s_common.page import Page
from explorer_s_common.decorator import common_ajax_response
from explorer_s_common.utils import format_return, format_price, type_filter, prams_filter
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
def search_notice(request):
    title = request.POST.get('title')
    state = request.POST.get('state', '-9')
    state = None if state == '-9' else state
    page_index = int(request.POST.get('page_index', 1))
    page_count = min(int(request.POST.get('page_count', 10)), 50)

    objs = NoticeBase().search_for_admin(title=title, state=state)
    data = Page(objs, page_count).page(page_index)

    return format_return(0, data={
        'objs': format_notice(data['objects']), 'total_page': data['total_page'], 'total_count': data['total_count']
    })


@common_ajax_response
def get_notice_by_id(request):
    obj_id = request.POST.get('obj_id')
    notice = NoticeBase().get_notice_by_id(obj_id=obj_id)

    return format_return(0, data=format_notice(notice))


@common_ajax_response
def add_notice(request):
    publish_time = request.POST.get('publish_time')
    title = request.POST.get('title')
    content = request.POST.get('content')
    category = request.POST.get('category', 0)
    author = request.POST.get('author')
    sort = request.POST.get('sort', 0)
    state = request.POST.get('state', 0)

    return NoticeBase().add_notice(
        publish_time=publish_time, title=title, content=content, category=category,
        author=author, sort=sort, state=state
    )


@common_ajax_response
def modify_notice(request):
    obj_id = request.POST.get('obj_id')
    publish_time = request.POST.get('publish_time')
    title = request.POST.get('title')
    content = request.POST.get('content')
    category = request.POST.get('category', 0)
    author = request.POST.get('author')
    sort = request.POST.get('sort', 0)
    state = request.POST.get('state', 0)

    return NoticeBase().modify_notice(
        obj_id=obj_id, publish_time=publish_time, title=title, content=content, category=category,
        author=author, sort=sort, state=state
    )


def format_faq(objs):
    if objs is None:
        return None

    def _format_obj(obj):
        return {
            'id': obj.id, 'title': obj.title, 'content': obj.content,
            'sort': obj.sort,"state":obj.state,
            'create_time': obj.create_time.strftime('%Y-%m-%d %H:%M:%S')
        }

    return [_format_obj(obj) for obj in objs] if isinstance(objs, Iterable) else _format_obj(objs)


@common_ajax_response
def search_faq(request):
    title = request.POST.get('title')
    page_index = int(request.POST.get('page_index', 1))
    page_count = min(int(request.POST.get('page_count', 10)), 50)
    start_time = request.POST.get("start_time")
    id = request.POST.get("id")
    end_time = request.POST.get("end_time")
    state = request.POST.get("state")
    delete_key_list, error_field = type_filter(type_filter=["state"], **request.POST.dict())
    if delete_key_list is None:
        return format_return(15000, msg="缺少字段:{}".format(error_field))
    prams_dict = prams_filter(delete_key_list=delete_key_list, title__icontains=title, id=id,
                              create_time__gte=start_time, create_time__lte=end_time, state=state)

    objs = FaqBase().search_for_admin(**prams_dict)
    data = Page(objs, page_count).page(page_index)

    return format_return(0, data={
        'objs': format_faq(data['objects']), 'total_page': data['total_page'], 'total_count': data['total_count']
    })


@common_ajax_response
def get_faq_by_id(request):
    obj_id = request.POST.get('obj_id')
    faq = FaqBase().get_faq_by_id(obj_id)

    return format_return(0, data=format_faq(faq))


@common_ajax_response
def add_faq(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    sort = request.POST.get('sort', '0')

    return FaqBase().add_faq(title=title, content=content, sort=sort)


@common_ajax_response
def modify_faq(request):
    obj_id = request.POST.get('obj_id')
    title = request.POST.get('title')
    content = request.POST.get('content')
    sort = request.POST.get('sort', '0')
    state = request.POST.get('state', 1)
    return FaqBase().modify_faq(obj_id=obj_id, title=title, content=content, sort=sort, state=state)


@common_ajax_response
def delete_faq(request):
    obj_id = request.POST.get('obj_id')
    faq = FaqBase().get_faq_by_id(obj_id)
    if not faq:
        return format_return(15000)
    else:
        faq.delete()
        return format_return(0)
