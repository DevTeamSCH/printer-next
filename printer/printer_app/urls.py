from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework import routers

from printer_app.views import logout_view
from . import views

router = routers.DefaultRouter()
router.register(r'api/v1/my-printers', views.UserPrinterViewSet, base_name="printer")
router.register(r'api/v1/active-printers', views.PrinterListView, base_name="active-printer")

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('logout/', logout_view,  name='logout'),
    path('new-printer', login_required(views.NewPrinterView.as_view()), name="new-printer"),
    path('delete-printer', login_required(views.DeletePrinterView.as_view()), name="delete-printer"),
    path('client', views.ClientView.as_view(), name='client'),
    path('FAQ', views.FAQView.as_view(), name='FAQ'),
    path('profile', login_required(views.ProfileView.as_view()), name='profile'),
    path('get-room', login_required(views.GetRoomView.as_view()), name='get-room'),
    path('generate-token', login_required(views.GenerateTokenView.as_view()), name='generate-token'),
    path('file-upload', login_required(views.FileView.as_view()), name='file-upload'),
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
]
