import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


# TODO: Change to profile
class User(AbstractUser):
    room = models.CharField(max_length=255, default="", verbose_name=_("Room number"))

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()

    @property
    def printers(self):
        return self.owned_printers.all()

    @property
    def active_printers(self):
        return self.owned_printers.filter(status=True)

    @property
    def has_active_printers(self):
        return any(printer.status for printer in self.printers)


class Printer(models.Model):
    TYPE_CHOICES = (
        ("BW", _("Black-White")),
        ("CL", _("Color"))
    )

    owner = models.ForeignKey(
        User,
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
        User,
        related_name='owned_files',
        on_delete=models.CASCADE
    )
    shared_with = models.ManyToManyField(
        User,
        related_name='shared_files'
    )
    uploaded = models.DateTimeField(auto_now_add=True)


#Deletes file from filesystem when File object is deleted.
@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
