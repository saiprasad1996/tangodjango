from django.conf.urls import url,include

from . import views

urlpatterns =[
    url(r'^$',views.pleaseInfo),
    url(r'^askus$',views.postquestion),
    url(r'^questions$',views.showQuestions),
    url(r'^collab/auth$',views.auth),
    url(r'^collab/auth/redirect$',views.collab_redirect),
    url(r'^collab/broadcast$',views.collab_broadcast),
    url(r'^collab/fbauth$',views.fbauth),
    url(r'^collab/fbregister',views.user_register_fb,name="fb_register")
    


]
