from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    room = models.CharField(max_length=255, default="")
    status = models.BooleanField(default=True)

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
    def has_active_printers(self):
        return any(printer.status for printer in self.printers)


class Printer(models.Model):
    TYPE_CHOICES = (
        ("BW", "Black-White"),
        ("CL", "Color")
    )

    owner = models.ForeignKey(
        User,
        related_name='owned_printers',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    status = models.BooleanField(default=False)
    comment = models.TextField(null=True, blank=True)
