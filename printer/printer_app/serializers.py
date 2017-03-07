from printer_app.models import User, Printer
from rest_framework import serializers


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = ('id', 'name', 'status')


class UserPrinterSerializer(serializers.ModelSerializer):
    printers = PrinterSerializer(many=True)

    class Meta:
        model = User
        fields = ['printers']
