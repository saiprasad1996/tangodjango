from django.conf.urls import url,include

from . import views

urlpatterns =[
    url(r'^$',views.testdoc,name='testdoc'),
    url(r'^company/(?P<pk>\d+)/$',views.companydetails,name='testdoc'),
    url(r'^company/new/$',views.company_new,name='company_new')

]
