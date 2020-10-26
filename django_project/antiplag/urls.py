from django.urls import path
from antiplag import views


urlpatterns = [
    path('files/', views.file_list),
    path('files/<int:pk>/', views.file_detail),
]