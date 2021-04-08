from django.urls import path

from . import views

urlpatterns = [
    path("stats/", views.Stats.as_view()),
    path("submissions/", views.SubmissionList.as_view()),
    path("submissions/<int:id>", views.SubmissionDetail.as_view()),
    path("submissions/<int:id>/graph", views.SubmissionGraphDetail.as_view()),
    path("documents/<int:id>", views.DocumentDetail.as_view()),
    path("documents/<int:first_id>/diff/<second_id>", views.DocumentDiff.as_view()),
]
