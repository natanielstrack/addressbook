from django.conf.urls import url
from maps import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^add$', views.AddAddress.as_view(), name='addaddress'),
    url(r'^delete$', views.DeleteAddress.as_view(), name='delete'),
]
