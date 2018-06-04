from django.contrib import admin
from . import models


@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    filter_horizontal = ('shared_with',)


# Register your models here.
admin.site.register(models.Printer)
