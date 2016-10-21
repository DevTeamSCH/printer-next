from django.db import models


class User(models.Model):
    appkey = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    room = models.CharField(max_length=255)

    # Kilistáza a felhasználó összes nyomtatóját
    @property
    def printers(self):
        return self.owned_printers.all()

    # Akkor False ha a felhasználó egytlen nyomtatója se aktív
    @property
    def is_active(self):
        return any(printer.status for printer in self.printers)


class Printer(models.Model):
    TYPE_CHOICES = (
            ("BW", "Fekete-fehér"),
            ("CL", "Színes")
    );

    owner = models.ForeignKey(User, related_name='owned_printers')
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    status = models.BooleanField(default=False)
    comment = models.CharField(max_length=255, default="")
