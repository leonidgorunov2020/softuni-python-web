from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductReview(TemplateView):
    template_name = 'main/product_review.html'


class ServiceReview(TemplateView):
    template_name = 'main/service_review.html'


class JobReview(TemplateView):
    template_name = 'main/job_review.html'


class BecomeDev(TemplateView):
    template_name = 'main/become_dev.html'


class About(TemplateView):
    template_name = 'main/about.html'


def error_404(request, exception):
   context = {}
   return render(request, 'main/404.html', context)

def error_500(request):
   context = {}
   return render(request, 'main/500.html', context)
