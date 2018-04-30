import os
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from account.models import Profile


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


class File(models.Model):
    file = models.FileField(upload_to="")
    owner = models.ForeignKey(
        Profile,
        related_name='owned_files',
        on_delete=models.CASCADE
    )
    shared_with = models.ManyToManyField(
        Profile,
        related_name='shared_files'
    )
    uploaded = models.DateTimeField(auto_now_add=True)


# Deletes file from filesystem when File object is deleted.
@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
