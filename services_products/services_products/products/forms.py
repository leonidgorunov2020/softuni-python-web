from django import forms

from services_products.products.helpers import BootstrapFormMixin, DisabledFieldsFormMixin
from services_products.products.models import Product


class CreateProductForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        product = super().save(commit=False)
        product.user = self.user
        if commit:
            product.save()

            return product

    class Meta:
        model = Product
        fields = ('name', 'description', 'screenshot', 'type', 'price')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter product name',
                    'class': 'myfieldclass',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Describe your product',
                }
            ),
            'price': forms.TextInput(
                attrs={
                    'placeholder': 'Add price',
                }
            ),
        }


class EditProductForm(BootstrapFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Product
        fields = ('name', 'description', 'screenshot', 'type', 'price')


class DeleteProductForm(BootstrapFormMixin, DisabledFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Product
        fields = ('name', 'description', 'screenshot', 'type', 'price')
