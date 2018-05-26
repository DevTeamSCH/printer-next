from django.core import exceptions
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


@deconstructible
class FileSizeValidator():
    size_limit = 5242880  # 5MB - 5242880
    message = _('Too big file. %(size)d')
    code = 'invalid'

    def __init__(self, size_limit=None, message=None, code=None):
        if size_limit is not None:
            self.size_limit = size_limit
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, file):
        if file.size > self.size_limit:
            raise exceptions.ValidationError(
                self.message,
                code=self.code,
                params={'size': file.size}
            )
