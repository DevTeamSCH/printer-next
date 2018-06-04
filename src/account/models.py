from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    room = models.CharField(max_length=255, default="", verbose_name=_("Room number"))
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)

    def get_full_name(self):
        full_name = f"{self.user.last_name} {self.user.first_name}"
        return full_name.strip()

    def __str__(self):
        return self.get_full_name()

    @property
    def printers(self):
        return self.owned_printers.all()

    @property
    def active_printers(self):
        return self.owned_printers.filter(status=True)

    @property
    def has_active_printers(self):
        return any(printer.status for printer in self.printers)
