import os
import shutil
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import FileExtensionValidator

from account.models import Profile
from . import validators


class Printer(models.Model):
    TYPE_CHOICES = (
        ("BW", _("Black-White")),
        ("CL", _("Color"))
    )

    owner = models.ForeignKey(
        Profile,
        related_name='owned_printers',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, verbose_name=_("Type"))
    status = models.BooleanField(default=False, verbose_name=_("Available"))
    comment = models.TextField(null=True, blank=True, verbose_name=_("Comment"))

    def __str__(self):
        return self.name


class File(models.Model):
    file = models.FileField(
        validators=[
            validators.FileSizeValidator(52428800),  # 50MB
            # TODO: Combine with validate_image_file_extension
            FileExtensionValidator(allowed_extensions=['doc', 'docx', 'odt', 'djvu', 'jpg', 'jpeg', 'pdf', 'png'])
        ],
        verbose_name=_("File")
    )
    owner = models.ForeignKey(
        Profile,
        related_name='owned_files',
        on_delete=models.CASCADE,
        verbose_name=_("Owner")
    )
    shared_with = models.ManyToManyField(
        Profile,
        blank=True,
        related_name='shared_files',
        verbose_name=_("Shared With")
    )
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class FaqEntry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.title


# Deletes file from filesystem when File object is deleted.
@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=File)
def auto_delete_old_files(sender, instance, **kwargs):
    """ This handler delete old files when need it. """
    free_space = shutil.disk_usage(settings.MEDIA_ROOT).free
    files = File.objects.all().order_by('uploaded')

    # TODO: Problem when not enough the free space and there are no uploaded files
    while free_space < instance.file.size:
        files[0].delete()
        free_space = shutil.disk_usage(settings.MEDIA_ROOT).free
