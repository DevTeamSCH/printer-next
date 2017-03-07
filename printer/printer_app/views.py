from django.contrib.auth import logout
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import RedirectView
from django.shortcuts import redirect, get_object_or_404
from printer_app import models
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.response import Response

from printer_app.forms import NewPrinterForm, GetRoomForm
from printer_app.models import Printer
from printer_app.serializers import UserPrinterSerializer, PrinterSerializer
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

    def user_name(self):
        return self.request.user.get_full_name()

    def user_room(self):
        if self.request.user.room == "":
            return "Nincs megadva"
        else:
            return self.request.user.room


class NewPrinterView(CreateView):
    model = models.Printer
    form_class = NewPrinterForm
    template_name = "printer_create.html"
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        if request.user.room == "":
            return redirect(reverse_lazy("get-room") + "?next=new-printer")
        else:
            return super(NewPrinterView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(NewPrinterView, self).form_valid(form)


class GetRoomView(UpdateView):
    model = models.User
    form_class = GetRoomForm
    template_name = "get_room.html"

    def get_object(self):
        self.success_url = reverse_lazy(self.request.GET.get('next', 'profile'))
        return self.request.user


class GenerateTokenView(RedirectView):
    url = 'profile'

    def get_redirect_url(self, *args, **kwargs):
        Token.objects.filter(user=self.request.user).delete()
        Token.objects.create(user=self.request.user)
        return super(GenerateTokenView, self).get_redirect_url(*args, **kwargs)


class UserPrinterViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = request.user.printers
        serializer = PrinterSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            printer = models.Printer.objects.get(pk=pk)
        except models.models.ObjectDoesNotExist:
            return Response("Requested object does not exist", 404)
        if printer.owner == request.user:
            serializer = PrinterSerializer(printer)
            return Response(serializer.data)
        return Response("Requested printer does not belong to this user", 403)

    def update(self, request, pk=None):
        try:
            printer = models.Printer.objects.get(pk=pk)
        except models.models.ObjectDoesNotExist:
            return Response("Requested object does not exist", 404)
        if printer.owner == request.user:
            serializer = PrinterSerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            printer.status = serializer.validated_data['status']
            printer.save()
            return Response("ok")
        return Response("Requested printer does not belong to this user", 403)


def logout_view(request):
    logout(request)
    return redirect("index")
