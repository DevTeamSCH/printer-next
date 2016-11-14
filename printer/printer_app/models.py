from django.db import models
from authsch.models import AbstractAuthSchBase


class User(AbstractAuthSchBase):
    appkey = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    room = models.CharField(max_length=255)

    @property
    def printers(self):
        return self.owned_printers.all()

    @property
    def is_active(self):
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
