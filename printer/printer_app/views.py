from django.views import generic
from printer_app import models


class IndexView(generic.TemplateView):
    template_name = "printer_app/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['users'] = models.User.objects.all()
        return context
