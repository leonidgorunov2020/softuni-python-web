from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, TemplateView

from services_products.accounts.forms import CreateProfileForm
from services_products.accounts.helpers import BootstrapFormMixin
from services_products.accounts.models import Profile


class UserLoginView(LoginView):
    template_name = 'accounts/login_page.html'
    success_url = reverse_lazy('show index')

    def get_success_url(self):
        if self.success_url:
            return self.success_url

        return super().get_success_url()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('show index')

        return super().dispatch(request, *args, **kwargs)


class UserRegisterView(CreateView):
    form_class = CreateProfileForm
    template_name = 'accounts/profile_create.html'
    success_url = reverse_lazy('show index')


class UserDetailsView(DetailView):
    model = Profile
    template_name = 'accounts/profile_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user == self.request.user
        return context


class EditUserView(BootstrapFormMixin, UpdateView):
    model = Profile
    fields = ('first_name', 'last_name', 'picture',
              'date_of_birth', 'personal_info', 'email', 'gender')
    template_name = 'accounts/profile_edit.html'

    def form_valid(self, form):
        item = form.save()
        self.pk = item.pk
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile view', kwargs={'pk': self.pk})


class ChangeUserPasswordView(PasswordChangeView):
    template_name = 'accounts/profile_change_password.html'

    def form_valid(self, form):
        item = form.save()
        self.pk = item.pk
        return super().form_valid(form)

    def get_success_url(self):
        # print(self.pk)
        return reverse('profile view', kwargs={'pk': self.pk})


class DeleteUserView(DeleteView):
    model = Profile
    template_name = 'accounts/profile_delete.html'
    success_url = reverse_lazy('show index')


class LastViewedProduct(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/last_viewed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'last_viewed_product' in self.request.session:
            context['last_viewed_product'] = self.request.session['last_viewed_product']
        if 'last_viewed_service' in self.request.session:
            context['last_viewed_service'] = self.request.session['last_viewed_service']
        if 'last_viewed_job' in self.request.session:
            context['last_viewed_job'] = self.request.session['last_viewed_job']
        return context





