from django.conf.urls import url, include
from django.contrib import admin
from browser.views import *

urlpatterns = [
    url(r'^paychecker/', include('browser.urls')),
]
