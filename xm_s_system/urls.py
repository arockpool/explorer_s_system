from django.conf.urls import url, include

urlpatterns = [
    url(r'^system/api/', include('system.urls')),
    url(r'^system/admin/', include('system.urls_admin')),

    url(r'^system/api/monitor/', include('monitor.urls')),

    url(r'^system/api/notice/', include('notice.urls')),
    url(r'^system/admin/notice/', include('notice.urls_admin')),
]
