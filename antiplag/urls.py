from django.urls import path

from . import views

urlpatterns = [
    path("submissions/", views.SubmissionList.as_view()),
    path("submissions/<int:id>", views.SubmissionDetail.as_view()),
    path("documents/<int:id>", views.DocumentDetail.as_view()),
]
