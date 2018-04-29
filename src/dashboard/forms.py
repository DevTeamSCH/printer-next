from django import forms

from . import models

base_classes = 'uk-form-width-medium uk-form-small'


class NewPrinterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewPrinterForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'class': base_classes + ' uk-input'}
        self.fields['type'].widget.attrs = {'class': base_classes + ' uk-select'}
        self.fields['comment'].widget.attrs = {'class': base_classes + ' uk-textarea'}

    class Meta:
        model = models.Printer
        fields = ['name', 'type', 'comment']


class GetRoomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GetRoomForm, self).__init__(*args, **kwargs)
        self.fields['room'].widget.attrs = {'class': base_classes + ' uk-input'}

    class Meta:
        model = models.User
        fields = ['room']


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = models.File
        fields = ['file']
