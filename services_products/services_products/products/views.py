from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from services_products.products.forms import CreateProductForm, EditProductForm, DeleteProductForm
from services_products.products.models import Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    template_name = 'products/product_create.html'
    form_class = CreateProductForm
    success_url = reverse_lazy('list products')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ProductListView(ListView):
    paginate_by = 8
    model = Product
    template_name = 'products/products_list.html'
    ordering = '-date_of_release'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = len(Product.objects.filter(type="Module"))
        context['plugins'] = len(Product.objects.filter(type="Plugin"))
        context['templates'] = len(Product.objects.filter(type="Template"))
        context['others'] = len(Product.objects.filter(type="Other"))

        return context


class ProductDetailsView(DetailView):
    model = Product
    template_name = 'products/product_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user == self.request.user
        self.request.session['last_viewed_product'] = (self.kwargs['pk'])
        return context


class EditProductView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = EditProductForm
    template_name = 'products/product_edit.html'
    success_url = reverse_lazy('list products')

    def get_success_url(self):
        if self.success_url:
            return self.success_url

        return super().get_success_url()


class DeleteProductView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_delete.html'
    form_class = DeleteProductForm

    success_url = reverse_lazy('show index')

    def get_success_url(self):
        if self.success_url:
            return self.success_url

        return super().get_success_url()


class ViewOwnProductList(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/products_view_own.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(user_id=self.request.user.id)
        context['modules'] = len(Product.objects.filter(type="Module").filter(user_id=self.request.user.id))
        context['plugins'] = len(Product.objects.filter(type="Plugin").filter(user_id=self.request.user.id))
        context['templates'] = len(Product.objects.filter(type="Template").filter(user_id=self.request.user.id))
        context['others'] = len(Product.objects.filter(type="Other").filter(user_id=self.request.user.id))
        return context


