from django.conf.urls import url
from maps import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
]
