# example/urls.py
from django.urls import path

from orders.views import index


urlpatterns = [
    path("", index),
]
