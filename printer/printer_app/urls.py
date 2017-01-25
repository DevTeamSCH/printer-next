from django.conf.urls import url, include
from django.contrib.auth import logout
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'api', views.UserPrinterViewSet, base_name="printer")

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^newprinter', views.NewPrinterView.as_view(), name="newPrinter"),
    url(r'^client', views.ClientView.as_view(), name='client'),
    url(r'^FAQ', views.FAQView.as_view(), name='FAQ'),
    url(r'^profile', views.ProfileView.as_view(), name='profile'),
    url(r'^getroom', views.GetRoomView.as_view(), name='getroom'),
    url(r'^generateToken', views.GenerateTokenView.as_view(), name='generateToken'),
    url(r'^', include(router.urls)),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework'))
]
