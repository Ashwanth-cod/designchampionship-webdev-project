from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# -------------------------------
# User Profile
# -------------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    school_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"


# -------------------------------
# Startup Idea
# -------------------------------
class Idea(models.Model):
    CATEGORY_CHOICES = [
        ("tech", "Tech"),
        ("entertainment", "Entertainment"),
        ("education", "Education"),
        ("health", "Health"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    description = models.TextField(max_length=1000)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ideas')
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # exclude current instance (important for updates)
            while Idea.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# -------------------------------
# Comments
# -------------------------------
class Comment(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user.username} on {self.idea.name}"


# -------------------------------
# Likes
# -------------------------------
class Like(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["idea", "user"], name="unique_like")
        ]

    def __str__(self):
        return f"{self.user.username} likes {self.idea.name}"


# -------------------------------
# Ratings
# -------------------------------
class Rating(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField()  # 1–5 rating
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["idea", "user"], name="unique_rating")
        ]

    def __str__(self):
        return f"{self.value}⭐ by {self.user.username} on {self.idea.name}"
