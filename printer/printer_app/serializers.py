from rest_framework.fields import SerializerMethodField

from printer_app.models import User, Printer
from rest_framework import serializers


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = ('id', 'name', 'status', 'type', 'comment')


class UserSerializer(serializers.ModelSerializer):
    name = SerializerMethodField()

    class Meta:
        model = User
        fields = ('name', 'room')

    def get_name(self, user):
        return user.get_full_name()


class ActivePrinterSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Printer
        fields = ('name', 'comment', 'type', 'owner')