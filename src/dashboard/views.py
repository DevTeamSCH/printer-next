from django.contrib.auth import logout, mixins
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import base, edit, list
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authtoken.models import Token

from . import models
from . import forms
from . import serializers
from account.models import Profile


class IndexView(base.TemplateView):
    template_name = "dashboard/printer_list.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['profiles'] = Profile.objects.all()
        return context


class FAQView(list.ListView):
    template_name = "dashboard/faq.html"
    model = models.FaqEntry


class ProfileView(mixins.LoginRequiredMixin, base.TemplateView):
    template_name = "dashboard/profile.html"
    printer_form_set = inlineformset_factory(
        Profile,
        models.Printer,
        form=forms.NewPrinterForm,
        extra=0,
        can_delete=False,
        fields=('name', 'status', 'type', 'comment')
    )

    def get_formset(self):
        return self.printer_form_set(instance=self.request.user.profile)

    def token(self):
        return Token.objects.get_or_create(user=self.request.user)[0]

    def user_name(self):
        return self.request.user.profile.get_full_name()

    def user_room(self):
        if self.request.user.profile.room == "":
            return _("N/A")
        else:
            return self.request.user.profile.room

    def post(self, request):
        formset = self.printer_form_set(request.POST, request.FILES, instance=self.request.user.profile)
        if formset.is_valid():
            formset.save()
            return redirect("profile")


class NewPrinterView(mixins.LoginRequiredMixin, edit.CreateView):
    model = models.Printer
    form_class = forms.NewPrinterForm
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        if request.user.profile.room == "":
            return redirect(reverse_lazy("get-room") + "?next=new-printer")
        else:
            return super(NewPrinterView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super(NewPrinterView, self).form_valid(form)


class GetRoomView(mixins.LoginRequiredMixin, edit.UpdateView):
    model = Profile
    form_class = forms.GetRoomForm
    template_name = "dashboard/get_room.html"

    def get_object(self):
        self.success_url = reverse_lazy(self.request.GET.get('next', 'profile'))
        return self.request.user.profile


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
        return self.request.user.profile.printers

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.profile)


def logout_view(request):
    logout(request)
    return redirect("index")


class PrinterDeleteView(mixins.LoginRequiredMixin, edit.DeleteView):
    model = models.Printer
    success_url = reverse_lazy("profile")


class PrinterListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = Profile.objects.all()


class FileView(mixins.LoginRequiredMixin, base.TemplateView):
    template_name = 'dashboard/files.html'

    def get_context_data(self, **kwargs):
        context = super(FileView, self).get_context_data(**kwargs)
        context['form'] = forms.FileUploadForm()
        context['uploaded_files'] = models.File.objects.filter(owner=self.request.user.profile)
        context['shared_files'] = self.request.user.profile.shared_files.all()
        return context


class FileUploadView(mixins.LoginRequiredMixin, edit.CreateView):
    model = models.File
    form_class = forms.FileUploadForm
    success_url = reverse_lazy('files')

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)


class FileDeleteView(mixins.LoginRequiredMixin, edit.DeleteView):
    model = models.File
    success_url = reverse_lazy("files")


class SharedWithView(mixins.LoginRequiredMixin, edit.UpdateView):
    model = models.File
    form_class = forms.SharedWithForm
    success_url = reverse_lazy('files')
