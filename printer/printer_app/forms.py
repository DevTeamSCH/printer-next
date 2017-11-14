from django.forms import ModelForm

from printer_app.models import Printer, User, File

base_classes = 'uk-form-width-medium uk-form-small'


class NewPrinterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewPrinterForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'class': base_classes + ' uk-input'}
        self.fields['type'].widget.attrs = {'class': base_classes + ' uk-select'}
        self.fields['comment'].widget.attrs = {'class': base_classes + ' uk-textarea'}

    class Meta:
        model = Printer
        fields = ['name', 'type', 'comment']


class GetRoomForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(GetRoomForm, self).__init__(*args, **kwargs)
        self.fields['room'].widget.attrs = {'class': base_classes + ' uk-input'}

    class Meta:
        model = User
        fields = ['room']


class FileUploadForm(ModelForm):
    class Meta:
        model = File
        fields = ['file']
