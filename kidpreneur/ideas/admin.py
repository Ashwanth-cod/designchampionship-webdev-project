from django.contrib import admin
from .models import Idea, Comment, Like, Rating

admin.site.register(Idea)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Rating)
