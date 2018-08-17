from django import forms
from django.forms import BooleanField

from . import models
from account.models import Profile

base_classes = 'uk-form-width-medium uk-form-small'


class NewPrinterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {
            'class': f"{base_classes} uk-input"
        }
        self.fields['type'].widget.attrs = {
            'class': f"{base_classes} uk-select"
        }
        self.fields['comment'].widget.attrs = {
            'class': f"{base_classes} uk-textarea"
        }

    class Meta:
        model = models.Printer
        fields = ['name', 'type', 'comment']


class GetRoomForm(forms.ModelForm):
    data_handling = BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].widget.attrs = {
            'class': f"{base_classes} uk-input"
        }

    class Meta:
        model = Profile
        fields = ['room']


class FileUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        shared_with = self.fields['shared_with']
        shared_with.widget.attrs = {
            'class': f"{base_classes} uk-select"
        }
        choices = [(p.id, p.get_full_name()) for p in Profile.objects.all() if p.has_active_printers]
        shared_with.choices = choices

    class Meta:
        model = models.File
        fields = ['file', 'shared_with']


class SharedWithForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        shared_with = self.fields['shared_with']
        shared_with.widget.attrs = {
            'class': f"{base_classes} uk-select"
        }
        choices = [(p.id, p.get_full_name()) for p in Profile.objects.all() if p.has_active_printers]
        shared_with.choices = choices

    class Meta:
        model = models.File
        fields = ['shared_with']
