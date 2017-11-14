from rest_framework import routers

from django.conf.urls import url, include
from maps import views

router = routers.DefaultRouter()
router.register(r'address', views.AddressViewSet)

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^api/', include(router.urls)),
]
