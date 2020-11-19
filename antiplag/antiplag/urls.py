from django.conf.urls import url
from .views import file_detail


urlpatterns = [
    url(r"^upload/$", file_detail().as_view(), name="file-upload"),
]

