import json
import time
import datetime
from collections import Iterable

# from system.serializer import AdminSerializer
from system.models import ChoiceModel, Admin
from system.serializer import ChoiceSerializer,AppinfoSerializer
from explorer_s_common.decorator import common_ajax_response
from explorer_s_common.utils import format_return, serializer_create_or_update
from explorer_s_common.page import Page
from explorer_s_common import inner_server

from explorer_s_system import consts
from system.interface import AdminBase,AppinfoBase


@common_ajax_response
def add_admin(request):
    '''
    添加管理员
    '''
    user_id = request.POST.get('user_id')
    permissions = request.POST.get('permissions')

    return AdminBase().add_admin(user_id=user_id, permissions=permissions)


@common_ajax_response
def add_admin_by_role(request):
    '''
    根据角色添加管理员
    '''
    user_id = request.POST.get('user_id')
    role = request.POST.get('role', 'role_buyer')
    permissions = json.dumps(consts.ROLE_PERMESSIONS.get(role, []))
    return AdminBase().add_admin(user_id=user_id, permissions=permissions)


@common_ajax_response
def add_admin_super_super(request):
    '''
    添加管理员
    '''
    user_id = request.POST.get('user_id')
    permissions = request.POST.get('permissions', '[]')
    is_super = int(request.POST.get('is_super'))
    return AdminBase().add_admin(user_id=user_id, permissions=permissions, is_super=is_super)


@common_ajax_response
def get_admin_permissions(request):
    '''
    获取管理员权限
    '''
    user_id = request.POST.get('user_id')
    is_super = False
    permissions = []

    admin = AdminBase().get_admin_by_user_id(user_id=user_id)
    if not admin:
        return format_return(0, data={
            'user_id': user_id, 'is_super': is_super, 'permissions': permissions
        })

    is_super = admin.is_super
    # 如果是超级管理员
    if is_super:
        permissions = [p['code'] for p in consts.PERMESSIONS if p['parent']]
    else:
        permissions = json.loads(admin.permissions or "[]")

    return format_return(0, data={
        'user_id': user_id, 'is_super': is_super, 'permissions': permissions
    })


@common_ajax_response
def get_admins(request):
    '''
    获取所有管理员
    '''

    data = []
    for per in AdminBase().get_admins():
        user = inner_server.get_user_profile(user_id=per.user_id)
        data.append({
            'user_id': per.user_id,
            'avatar': user.get('avatar'),
            'nick': user.get('nick'),
            'mobile': user.get('mobile'),
            'create_time': per.create_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    return format_return(0, data=data)


@common_ajax_response
def modify_admin_permissions(request):
    '''
    修改用户权限
    '''
    user_id = request.POST.get('user_id')
    permissions = request.POST.get('permissions')

    return AdminBase().modify_admin_permissions(user_id=user_id, permissions=permissions)


@common_ajax_response
def remove_admin(request):
    '''
    删除管理员
    '''
    user_id = request.POST.get('user_id')

    return AdminBase().remove_admin(user_id=user_id)


@common_ajax_response
def get_all_permissions(request):
    '''
    获取所有权限
    '''
    return format_return(0, data=consts.PERMESSIONS)


@common_ajax_response
def get_admin_user_id_list(requests):
    query_set = AdminBase().get_common_admins()
    # serializer = AdminSerializer(query_set, many=True)

    return format_return(0, data=list(query_set.values_list('user_id', flat=True)))


@common_ajax_response
def get_super_admin_user_id_list(requests):
    query_set = AdminBase().get_super_admins()
    # serializer = AdminSerializer(query_set, many=True)

    return format_return(0, data=list(query_set.values_list('user_id', flat=True)))


@common_ajax_response
def get_config(request):
    page_index = int(request.POST.get('page_index', 1))
    page_count = min(int(request.POST.get('page_count', 10)), 50)
    key = request.POST.get('key')
    if key:
        obj = ChoiceModel.objects.filter(key=key, state=1)
    else:
        obj = ChoiceModel.objects.filter(state=1)
    serializer = ChoiceSerializer(obj, many=True)
    # data = Page(serializer.data, page_count).page(page_index)

    return format_return(0, data=serializer.data)
    # return format_return(0, data={
    #     'objs': data['objects'],
    #     'total_page': data['total_page'], 'total_count': data['total_count']
    # })


@common_ajax_response
def set_config(request):
    data_dict = request.POST.dict()
    serializer = ChoiceSerializer(data=data_dict)
    return serializer_create_or_update(serializer)


@common_ajax_response
def get_role_user_id(request):
    key = request.POST.get("key", "")
    objs = Admin.objects.filter(is_super=0, permissions__contains=key)
    return format_return(0, data=list(objs.values_list("user_id", flat=True)))


@common_ajax_response
def add_app_info(request):
    '''
    添加新appinfo
    '''
    user_id = request.user_id
    remarks = request.POST.get('remarks')
    result = AppinfoBase.add_app_info(user_id, remarks)
    if result:
        return format_return(0, data=result)
    return format_return(13004)


@common_ajax_response
def update_app_info(request):
    '''
    更新
    '''
    user_id = request.user_id
    # user_id = "b88c7ca4d7f711ebac9b0242ac160035"
    app_id = request.POST.get('app_id')
    remarks = request.POST.get('remarks')
    is_app_secret = int(request.POST.get('is_app_secret'))
    status = request.POST.get('status')
    result = AppinfoBase.update_app_info(app_id, user_id, is_app_secret, remarks, status)
    if result:
        return format_return(0, data=result)
    return format_return(13004)


@common_ajax_response
def get_app_infos(request):
    '''
    获取列表
    '''
    page_index = int(request.POST.get('page_index', 1))
    page_size = min(int(request.POST.get('page_size', 10)), 50)

    data_result = Page(AppinfoBase.get_app_infos(), page_size).page(page_index)
    data_result["objects"] = AppinfoSerializer(data_result["objects"], many=True).data
    return format_return(0, data=data_result)


# @common_ajax_response
# def del_app_info(request):
#     '''
#     删除
#     '''
#     app_id = request.POST.get('app_id')
#     user_id = request.user_id
#     data = AppinfoBase.del_app_info(app_id, user_id)
#     return format_return(0, data=data)