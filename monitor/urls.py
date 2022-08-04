from django.conf.urls import url

from monitor import views

urlpatterns = [
    # 慢请求相关
    url(r'^add_slow_request$', views.add_slow_request),
    url(r'^get_slow_request_group$', views.get_slow_request_group),
    url(r'^get_slow_request$', views.get_slow_request),

    # 系统错误相关
    url(r'^add_sys_error$', views.add_sys_error),
    url(r'^get_sys_error_group$', views.get_sys_error_group),
    url(r'^get_sys_error$', views.get_sys_error),

    # 请求日志相关
    url(r'^add_request_log$', views.add_request_log),
]
