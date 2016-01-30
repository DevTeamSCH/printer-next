from django.db import models


class User(models.Model):
    appkey = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)

    @property
    def printers(self):
        return self.owned_printers.all()

    @property
    def is_active(self):
        return any(printer.status for printer in self.printers)

class Printer(models.Model):
    owner = models.ForeignKey(User, related_name='owned_printers')
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
