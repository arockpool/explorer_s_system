"""
后台管理_公告,FAQ
"""
from django.conf.urls import url

from notice import views_admin

urlpatterns = [
    # notice
    url(r'^search_notice$', views_admin.search_notice),
    url(r'^get_notice_by_id$', views_admin.get_notice_by_id),
    url(r'^add_notice$', views_admin.add_notice),
    url(r'^modify_notice$', views_admin.modify_notice),

    # FAQ
    url(r'^search_faq$', views_admin.search_faq),
    url(r'^get_faq_by_id$', views_admin.get_faq_by_id),
    url(r'^add_faq$', views_admin.add_faq),
    url(r'^modify_faq$', views_admin.modify_faq),
    url(r'^delete_faq$', views_admin.delete_faq),
]
