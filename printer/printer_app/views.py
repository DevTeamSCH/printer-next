# from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import RedirectView
from django.shortcuts import redirect
from printer_app import models
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.response import Response
from printer_app.serializers import UserPrinterSerializer
from django.urls import reverse_lazy


class IndexView(generic.TemplateView):
    template_name = "printer_list.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['users'] = models.User.objects.all()
        return context


class ClientView(generic.TemplateView):
    template_name = "client.html"


class FAQView(generic.TemplateView):
    template_name = "faq.html"


class ProfileView(generic.TemplateView):
    template_name = "profile.html"

    def token(self):
        return Token.objects.get_or_create(user=self.request.user)[0]


class NewPrinterView(CreateView):
    model = models.Printer
    fields = ['name', 'type', 'comment']
    template_name = "printer_create.html"
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        if request.user.room == "":
            return redirect("get-room")
        else:
            return super(NewPrinterView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(NewPrinterView, self).form_valid(form)


class GetRoomView(UpdateView):
    model = models.User
    fields = ['room']
    template_name = "user_room_update.html"
    success_url = reverse_lazy("new-printer")

    def get_object(self):
        return self.request.user


class GenerateTokenView(RedirectView):
    url = 'profile'

    def get_redirect_url(self, *args, **kwargs):
        Token.objects.filter(user=self.request.user).delete()
        Token.objects.create(user=self.request.user)
        return super(GenerateTokenView, self).get_redirect_url(*args, **kwargs)


class UserPrinterViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = models.User.objects.filter(email=request.user.email)
        serializer = UserPrinterSerializer(queryset, many=True)
        return Response(serializer.data)


def logout_view(request):
    logout(request)
    return redirect("index")
