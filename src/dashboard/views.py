from django.contrib.auth import logout, mixins
from django.forms import inlineformset_factory
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import base, edit
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authtoken.models import Token

from . import models
from . import forms
from . import serializers


class IndexView(base.TemplateView):
    template_name = "printer_list.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['users'] = models.User.objects.all()
        return context


class ClientView(base.TemplateView):
    template_name = "client.html"


class FAQView(base.TemplateView):
    template_name = "faq.html"


class ProfileView(mixins.LoginRequiredMixin, base.TemplateView):
    template_name = "profile.html"
    printer_form_set = inlineformset_factory(
        models.User, models.Printer,
        form=forms.NewPrinterForm,
        extra=0,
        can_delete=False,
        fields=('name', 'status', 'type', 'comment')
    )

    def get_formset(self):
        return self.printer_form_set(instance=self.request.user)

    def token(self):
        return Token.objects.get_or_create(user=self.request.user)[0]

    def user_name(self):
        return self.request.user.get_full_name()

    def user_room(self):
        if self.request.user.room == "":
            return _("N/A")
        else:
            return self.request.user.room

    def post(self, request):
        formset = self.printer_form_set(request.POST, request.FILES, instance=self.request.user)
        if formset.is_valid():
            formset.save()
            return redirect("profile")


class NewPrinterView(mixins.LoginRequiredMixin, edit.CreateView):
    model = models.Printer
    form_class = forms.NewPrinterForm
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


class GetRoomView(mixins.LoginRequiredMixin, edit.UpdateView):
    model = models.User
    form_class = forms.GetRoomForm
    template_name = "get_room.html"

    def get_object(self):
        self.success_url = reverse_lazy(self.request.GET.get('next', 'profile'))
        return self.request.user


class GenerateTokenView(mixins.LoginRequiredMixin, base.RedirectView):
    url = 'profile'

    def get_redirect_url(self, *args, **kwargs):
        Token.objects.filter(user=self.request.user).delete()
        Token.objects.create(user=self.request.user)
        return super(GenerateTokenView, self).get_redirect_url(*args, **kwargs)


class UserPrinterViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PrinterSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.printers

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


def logout_view(request):
    logout(request)
    return redirect("index")


class DeletePrinterView(mixins.LoginRequiredMixin, edit.DeleteView):
    model = models.Printer
    success_url = reverse_lazy("profile")

    # def get_object(self, queryset=None):
    #    printer_id = self.request.GET.get('id', '')
    #    if printer_id == '':
    #        raise Http404
    #    try:
    #        printer = models.Printer.objects.get(pk=printer_id)
    #    except models.models.ObjectDoesNotExist:
    #        raise Http404
    #    if not printer.owner == self.request.user:
    #        raise Http404
    #    return printer


class PrinterListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()


class FileView(mixins.LoginRequiredMixin, base.TemplateView):
    template_name = 'file-upload.html'

    def get_context_data(self, **kwargs):
        context = super(FileView, self).get_context_data(**kwargs)
        context['form'] = forms.FileUploadForm()
        context['Files'] = models.File.objects.filter(owner=self.request.user)
        return context

    def post(self, request):
        form = forms.FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.owner = self.request.user
            form.save()
        return HttpResponseRedirect(reverse_lazy('file-upload'))
