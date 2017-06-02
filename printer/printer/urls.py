from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rosetta/', include('rosetta.urls')),
]

urlpatterns += i18n_patterns(
    url('', include('social_django.urls', namespace='social')),
    url(r'', include('printer_app.urls')),
    prefix_default_language=False
)
