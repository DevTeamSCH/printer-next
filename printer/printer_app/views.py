# from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from authsch.views import CallbackView
from printer_app import models
from django.conf import settings
import os
import binascii


class IndexView(generic.TemplateView):
    template_name = "printer_app/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['users'] = models.User.objects.all()
        state = binascii.hexlify(os.urandom(5)).decode()
        self.request.session['authsch_state'] = state
        context['url'] =  'https://auth.sch.bme.hu/site/login?response_type=code&client_id={client_code}&state={state}&scope={scopes}'.format(
            client_code=settings.AUTH_SCH['CLIENT_ID'],
            state=state,
            scopes='+'.join(settings.AUTH_SCH['SCOPES'])
        )
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

    def get(self, request, *args, **kwargs):
        if (request.user.room == ""):
            return redirect("/getroom")
        else:
            return super(NewPrinterView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = models.User.objects.get(id=1)
        return super(NewPrinterView, self).form_valid(form)


class GetRoomView(UpdateView):
    model = models.User
    fields = ['room']
    template_name_suffix = "_room_update"
    success_url = "/newprinter"


class LoginCallbackView(CallbackView):
    success_url = '/index'
    error_url = '/loginerror'

    def authentication_successful(self, profile, user):
        user.name = profile['displayName']
        user.email = profile['mail']
        user.room = ""
        user.save()
