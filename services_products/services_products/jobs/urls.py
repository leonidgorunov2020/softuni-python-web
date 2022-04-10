from django.urls import path

from services_products.jobs.views import JobCreateView, JobDetailsView, JobListView, EditJobView, DeleteJobView, \
    ViewOwnJobList

urlpatterns = [
    path('create', JobCreateView.as_view(), name="create job"),
    path('list', JobListView.as_view(), name="list jobs"),
    path('view/<int:pk>', JobDetailsView.as_view(), name="job details"),
    path('view/own/', ViewOwnJobList.as_view(), name='view own jobs'),
    path('edit/<int:pk>', EditJobView.as_view(), name="edit job"),
    path('delete/<int:pk>', DeleteJobView.as_view(), name="delete job")

]
