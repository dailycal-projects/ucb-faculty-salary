from django.conf.urls import url
from django.contrib import admin

from browser.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', SalaryRecordListView.as_view(), name='home'),
    url(r'^person/(?P<slug>[-\w]+)/$', PersonDetailView.as_view(), name='person_detail'),
    url(r'^departments/$', DepartmentListView.as_view(), name='department_list'),
    url(r'^departments/(?P<slug>[-\w]+)/$', DepartmentDetailView.as_view(), name='department_detail'),
]
