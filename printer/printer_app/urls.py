from django.conf.urls import url, include
from rest_framework import routers

from printer_app.views import logout_view
from . import views

router = routers.DefaultRouter()
router.register(r'api', views.UserPrinterViewSet, base_name="printer")

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^logout/$', logout_view,  name='logout'),
    url(r'^new-printer', views.NewPrinterView.as_view(), name="new-printer"),
    url(r'^client', views.ClientView.as_view(), name='client'),
    url(r'^FAQ', views.FAQView.as_view(), name='FAQ'),
    url(r'^profile', views.ProfileView.as_view(), name='profile'),
    url(r'^get-room', views.GetRoomView.as_view(), name='get-room'),
    url(r'^generate-token', views.GenerateTokenView.as_view(), name='generate-token'),
    url(r'^', include(router.urls)),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework'))
]
