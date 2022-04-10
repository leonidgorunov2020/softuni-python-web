from django import forms

from services_products.jobs.helpers import BootstrapFormMixin, DisabledFieldsFormMixin
from services_products.jobs.models import Job


class CreateJobForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        job = super().save(commit=False)
        job.user = self.user
        if commit:
            job.save()

            return job

    class Meta:
        model = Job
        fields = ('title', 'description', 'job_types', 'job_responsibilities', 'monthly_salary')
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Enter job title',
                    'class': 'myfieldclass',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Job details',
                }
            ),
            'monthly_salary': forms.TextInput(
                attrs={
                    'placeholder': 'Monthly salary',
                }
            ),
        }


class EditJobForm(BootstrapFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Job
        fields = ('title', 'description', 'job_types', 'job_responsibilities', 'monthly_salary')


class DeleteJobForm(BootstrapFormMixin, DisabledFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Job
        fields = ('title', 'description', 'job_types', 'job_responsibilities', 'monthly_salary')
