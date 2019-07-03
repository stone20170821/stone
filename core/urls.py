#! encodign:utf-8

from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^test/', test_logger),
    url(r'^chart/([0-9]*)/$', chart)
]
