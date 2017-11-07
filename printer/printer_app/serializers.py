from printer_app.models import User, Printer
from rest_framework import serializers


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = ('id', 'name', 'status', 'type', 'comment')

    def create(self, validated_data):
        data = validated_data
        data['owner'] = self.context.get('request').user
        return Printer.objects.create(**data)

