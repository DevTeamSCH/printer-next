# from django.contrib.auth.decorators import login_required
from django.views import generic

from printer_app import models


class IndexView(generic.TemplateView):
    template_name = "printer_app/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['users'] = models.User.objects.all()
        return context


class ClientView(generic.TemplateView):
    template_name = "printer_app/client.html"


class FAQView(generic.TemplateView):
    template_name = "printer_app/FAQ.html"


# @login_required
class ProfileView(generic.TemplateView):
    template_name = "printer_app/profile.html"
