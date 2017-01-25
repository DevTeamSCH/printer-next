from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'', include('printer_app.urls')),
    url('', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
]
