from django.urls import path

from . import views

urlpatterns = [
    path('submissions/', views.FileDetail.as_view()),
]
