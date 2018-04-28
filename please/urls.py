from django.conf.urls import url,include

from . import views

urlpatterns =[
    url(r'^$',views.pleaseInfo),
    url(r'^askus$',views.postquestion),
    url(r'^questions$',views.showQuestions),
    url(r'^collab/auth$',views.auth),
    url(r'^collab/auth/redirect$',views.collab_redirect),


]
