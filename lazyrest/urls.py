from django.conf.urls import url,include
from django.contrib.auth.models import User
from rest_framework import routers,serializers,viewsets

from .import views

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=User
        fields = ('url','username','email','is_staff')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

router = routers.DefaultRouter()
router.register(r'users',UserViewSet)

urlpatterns =[
    url(r'^',include(router.urls)),
]
