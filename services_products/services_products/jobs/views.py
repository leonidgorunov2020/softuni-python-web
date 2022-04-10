from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from services_products.jobs.forms import CreateJobForm, EditJobForm, DeleteJobForm
from services_products.jobs.models import Job


class JobCreateView(LoginRequiredMixin, CreateView):
    template_name = 'jobs/job_create.html'
    form_class = CreateJobForm
    success_url = reverse_lazy('list jobs')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class JobListView(ListView):
    paginate_by = 8
    model = Job
    template_name = 'jobs/jobs_list.html'
    ordering = '-date_of_publish'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['full_time'] = len(Job.objects.filter(job_types="Full Time"))
        context['part_time'] = len(Job.objects.filter(job_types="Part Time"))
        context['other'] = len(Job.objects.filter(job_types="Other"))
        return context


class JobDetailsView(DetailView):
    model = Job
    template_name = 'jobs/job_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user == self.request.user
        self.request.session['last_viewed_job'] = (self.kwargs['pk'])
        return context


class EditJobView(LoginRequiredMixin, UpdateView):
    model = Job
    form_class = EditJobForm
    template_name = 'jobs/job_edit.html'
    success_url = reverse_lazy('list jobs')

    def get_success_url(self):
        if self.success_url:
            return self.success_url

        return super().get_success_url()


class DeleteJobView(LoginRequiredMixin, DeleteView):
    model = Job
    template_name = 'jobs/job_delete.html'
    form_class = DeleteJobForm

    success_url = reverse_lazy('show index')

    def get_success_url(self):
        if self.success_url:
            return self.success_url

        return super().get_success_url()


class ViewOwnJobList(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'jobs/jobs_view_own.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobs'] = Job.objects.filter(user_id=self.request.user.id)
        context['part_time'] = len(Job.objects.filter(job_types="Part Time").filter(user_id=self.request.user.id))
        context['full_time'] = len(Job.objects.filter(job_types="Full Time").filter(user_id=self.request.user.id))
        context['other'] = len(Job.objects.filter(job_types="Other").filter(user_id=self.request.user.id))
        return context
