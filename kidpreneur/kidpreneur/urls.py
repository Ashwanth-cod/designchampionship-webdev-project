from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("veryserectadminthing/", admin.site.urls),
    path("", include("ideas.urls")),  # include app urls
]
