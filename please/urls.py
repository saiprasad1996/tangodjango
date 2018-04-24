from django.conf.urls import url,include

from . import views

urlpatterns =[
    url(r'^$',views.pleaseInfo),
    url(r'^askus$',views.postquestion),
    

]
