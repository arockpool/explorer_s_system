"""
后台管理_管理员管理
"""
from django.conf.urls import url

from system import views_admin

urlpatterns = [
    # 管理员
    url(r'^add_admin$', views_admin.add_admin),
    url(r'^add_admin_super_super$', views_admin.add_admin_super_super),  # 注册超级管理员
    url(r'^get_admin_user_id_list$', views_admin.get_admin_user_id_list),  # 获得所有管理员user_id
    url(r'^get_super_admin_user_id_list$', views_admin.get_super_admin_user_id_list),  # 获得所有超级管理员user_id
    url(r'^get_admin_permissions$', views_admin.get_admin_permissions),
    url(r'^get_admins$', views_admin.get_admins),
    url(r'^modify_admin_permissions$', views_admin.modify_admin_permissions),
    url(r'^remove_admin$', views_admin.remove_admin),
    url(r'^get_all_permissions$', views_admin.get_all_permissions),
    url(r'^add_admin_by_role$', views_admin.add_admin_by_role),
    url(r'^get_role_user_id$', views_admin.get_role_user_id),  # 获得有这个权限的用户user_id列表

    url(r'^get_config$', views_admin.get_config),  # 获取配置相关
    url(r'^set_config$', views_admin.set_config),  # 设置配置相关

    # App
    url(r'^add_app_info$', views_admin.add_app_info),
    url(r'^update_app_info$', views_admin.update_app_info),
    url(r'^get_app_infos$', views_admin.get_app_infos)

]
