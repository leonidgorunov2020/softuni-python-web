from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from services_products.services.forms import CreateServiceForm, EditServiceForm, DeleteServiceForm
from services_products.services.models import Service


class ServiceCreateView(LoginRequiredMixin, CreateView):
    template_name = 'services/service_create.html'
    form_class = CreateServiceForm
    success_url = reverse_lazy('list services')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ServiceListView(ListView):
    paginate_by = 8
    model = Service
    template_name = 'services/service_list.html'
    ordering = '-date_of_publish'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['one_time'] = len(Service.objects.filter(cycle="One Time"))
        context['weekly'] = len(Service.objects.filter(cycle="Weekly"))
        context['monthly'] = len(Service.objects.filter(cycle="Monthly"))
        context['other'] = len(Service.objects.filter(cycle="Other"))

        return context


class ServiceDetailsView(DetailView):
    model = Service
    template_name = 'services/service_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user == self.request.user
        self.request.session['last_viewed_service'] = (self.kwargs['pk'])
        return context


class EditServiceView(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = EditServiceForm
    template_name = 'services/service_edit.html'
    success_url = reverse_lazy('list services')

    def get_success_url(self):
        if self.success_url:
            return self.success_url

        return super().get_success_url()


class DeleteServiceView(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'services/service_delete.html'
    form_class = DeleteServiceForm

    success_url = reverse_lazy('show index')

    def get_success_url(self):
        if self.success_url:
            return self.success_url

        return super().get_success_url()

class ViewOwnServiceList(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'services/services_view_own.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(user_id=self.request.user.id)
        context['one_time'] = len(Service.objects.filter(cycle="One Time").filter(user_id=self.request.user.id))
        context['weekly'] = len(Service.objects.filter(cycle="Weekly").filter(user_id=self.request.user.id))
        context['monthly'] = len(Service.objects.filter(cycle="Monthly").filter(user_id=self.request.user.id))
        context['others'] = len(Service.objects.filter(cycle="Other").filter(user_id=self.request.user.id))
        return context

