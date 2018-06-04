from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'my-printers', views.UserPrinterViewSet, base_name="printer")
router.register(r'active-printers', views.PrinterListView, base_name="active-printer")

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('logout/', views.logout_view,  name='logout'),
    path('new-printer', views.NewPrinterView.as_view(), name="new-printer"),
    path('printer/<int:pk>/delete', views.PrinterDeleteView.as_view(), name="delete-printer"),
    path('client', views.ClientView.as_view(), name='client'),
    path('FAQ', views.FAQView.as_view(), name='FAQ'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('get-room', views.GetRoomView.as_view(), name='get-room'),
    path('generate-token', views.GenerateTokenView.as_view(), name='generate-token'),
    path('files', views.FileView.as_view(), name='files'),
    path('files/<int:pk>/delete', views.FileDeleteView.as_view(), name='file-delete'),
    path('file-upload', views.FileUploadView.as_view(), name='file-upload'),
    path('files/<int:pk>/share', views.SharedWithView.as_view(), name='file-share'),
    path('api/v1/', include(router.urls)),
]
