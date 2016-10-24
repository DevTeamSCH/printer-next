# from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic.edit import CreateView
from authsch.views import CallbackView
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


# @login_required
class NewPrinterView(CreateView):
    model = models.Printer
    fields = ['name', 'type', 'comment']
    template_name_suffix = '_create'
    success_url = '/index'

    def form_valid(self, form):
        form.instance.owner = models.User.objects.get(id=1)
        return super(NewPrinterView, self).form_valid(form)


class LoginCallbackView(CallbackView):
    success_url = '/index'
    error_url = '/index'

    def authentication_successful(self, profile, user):
        user.name = profile['basic']
        user.email = profile['mail']
        user.room = ""
