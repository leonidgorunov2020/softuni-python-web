from django import forms

from services_products.services.helpers import BootstrapFormMixin, DisabledFieldsFormMixin
from services_products.services.models import Service


class CreateServiceForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        service = super().save(commit=False)
        service.user = self.user
        if commit:
            service.save()

            return service

    class Meta:
        model = Service
        fields = ('name', 'description', 'cycle', 'fee')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter service name',
                    'class': 'myfieldclass',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Describe your service',
                }
            ),
            'fee': forms.TextInput(
                attrs={
                    'placeholder': 'Add fee',
                }
            ),
        }


class EditServiceForm(BootstrapFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Service
        fields = ('name', 'description', 'cycle', 'fee')


class DeleteServiceForm(BootstrapFormMixin, DisabledFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Service
        fields = ('name', 'description', 'cycle', 'fee')
