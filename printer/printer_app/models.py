from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class User(AbstractBaseUser):
    name = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    room = models.CharField(max_length=255, default="")
    status = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

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
