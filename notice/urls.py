from django.conf.urls import url

from notice import views

urlpatterns = [
    # 公告
    url(r'^get_notice_list$', views.get_notice_list),
    url(r'^get_notice_by_id$', views.get_notice_by_id),
    url(r'^get_notice_data_overview$', views.get_notice_data_overview),  # 矿工后台,dashoard_数据总览

    # FAQ
    url(r'^get_faq_list$', views.get_faq_list),
    url(r'^get_faq_by_id$', views.get_faq_by_id),

]
