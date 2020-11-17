from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from .views import index, file_list, file_detail
from django.urls import path
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('', index, name='index'),
    #path('file/', file_list.as_view()),
    #path('file/<int:pk>/', file_detail.as_view()),
    url(r'^upload/$', file_detail().as_view(), name='file-upload'),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
