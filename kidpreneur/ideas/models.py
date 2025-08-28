from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid

class Idea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ideas")
    title = models.CharField(max_length=200)
    problem = models.TextField()
    solution = models.TextField(blank=True)
    image = models.ImageField(upload_to="ideas/", blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + "-" + str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Like(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=1)  # 1–5


class Comment(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
