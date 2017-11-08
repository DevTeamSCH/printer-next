from rest_framework.fields import SerializerMethodField

from printer_app.models import User, Printer
from rest_framework import serializers


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = ('id', 'name', 'status', 'type', 'comment')


class UserSerializer(serializers.ModelSerializer):
    name = SerializerMethodField()
    active_printers = PrinterSerializer(many=True)

    class Meta:
        model = User
        fields = ('name', 'room', 'active_printers')

    def get_name(self, user):
        return user.get_full_name()
