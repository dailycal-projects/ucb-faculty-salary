from browser.views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^$', SalaryRecordListView.as_view(), name='home'),
    url(r'^context/$', ContextView.as_view(), name='context'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^person/(?P<slug>[-\w]+)/$', PersonDetailView.as_view(), name='person_detail'),
    url(r'^departments/$', DepartmentListView.as_view(), name='department_list'),
    url(r'^departments/(?P<slug>[-\w]+)/$', DepartmentDetailView.as_view(), name='department_detail'),
]
