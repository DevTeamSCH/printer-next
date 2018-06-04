import os
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
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


# Deletes file from filesystem when File object is deleted.
@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
