from printer_app.models import User
from rest_framework import serializers


class UserPrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('printers', 'status')
