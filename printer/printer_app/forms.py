from django.forms import ModelForm

from printer_app.models import Printer


class NewPrinterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewPrinterForm, self).__init__(*args, **kwargs)
        base_classes = 'uk-form-width-medium uk-form-small'
        self.fields['name'].widget.attrs = {'class': base_classes + ' uk-input'}
        self.fields['type'].widget.attrs = {'class': base_classes + ' uk-select'}
        self.fields['comment'].widget.attrs = {'class': base_classes + ' uk-textarea'}

    class Meta:
        model = Printer
        fields = ['name', 'type', 'comment']