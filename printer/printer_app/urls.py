from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from rest_framework import routers

from printer_app.views import logout_view
from . import views

router = routers.DefaultRouter()
router.register(r'api/my-printers', views.UserPrinterViewSet, base_name="printer")
router.register(r'api/active-printers', views.PrinterListView, base_name="active-printer")

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^logout/$', logout_view,  name='logout'),
    url(r'^new-printer', login_required(views.NewPrinterView.as_view()), name="new-printer"),
    url(r'^delete-printer', login_required(views.DeletePrinterView.as_view()), name="delete-printer"),
    url(r'^client', views.ClientView.as_view(), name='client'),
    url(r'^FAQ', views.FAQView.as_view(), name='FAQ'),
    url(r'^profile', login_required(views.ProfileView.as_view()), name='profile'),
    url(r'^get-room', login_required(views.GetRoomView.as_view()), name='get-room'),
    url(r'^generate-token', login_required(views.GenerateTokenView.as_view()), name='generate-token'),
    url(r'^', include(router.urls)),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
]