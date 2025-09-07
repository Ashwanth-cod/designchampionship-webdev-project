from django.contrib import admin
from django.urls import path, include  # include needed to pull in app urls

urlpatterns = [
    path('veryserectadminthing/', admin.site.urls),  # your admin path
    path('', include('ideas.urls')),  # include your app urls here
]
