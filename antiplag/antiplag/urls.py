from django.conf.urls import url
from .views import FileDetail


urlpatterns = [
    url(r"^upload/$", FileDetail().as_view(), name="file-upload"),
]

