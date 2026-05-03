from django.urls import path

from store_app.views import about, index


urlpatterns = [
    path("about/", about),
    path("", index),
]