from django.conf.urls import url

from system import views

urlpatterns = [
    url(r'^get_oss_sts$', views.get_oss_sts),

    url(r'^send_sms$', views.send_sms),
    url(r'^send_email$', views.send_email),

    url(r'^weixin/auth_by_code$', views.auth_by_code),
    url(r'^weixin/decrypt_data$', views.decrypt_data),
    url(r'^weixin/save_form_id$', views.save_form_id),
    url(r'^weixin/get_access_token$', views.get_access_token),

    url(r'^get_app_info$', views.get_app_info),
]
