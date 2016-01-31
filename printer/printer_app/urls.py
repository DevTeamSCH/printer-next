from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$|index', views.IndexView.as_view(), name='index'),
    url(r'client', views.ClientView.as_view(), name='client'),
    url(r'FAQ', views.FAQView.as_view(), name='FAQ'),
    url(r'profile', views.ProfileView.as_view(), name='profile'),
]
