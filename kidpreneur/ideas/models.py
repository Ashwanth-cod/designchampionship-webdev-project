from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify

# -------------------------
# Custom User
# -------------------------
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=True)
    is_student = models.BooleanField(default=False)
    school_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    @property
    def age(self):
        from datetime import date
        if self.dob:
            today = date.today()
            return today.year - self.dob.year - (
                (today.month, today.day) < (self.dob.month, self.dob.day)
            )
        return None

    def __str__(self):
        return self.username    


# -------------------------
# Idea Model
# -------------------------
class Idea(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Technology'),
        ('edu', 'Education'),
        ('art', 'Art'),
        ('other', 'Other')
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ideas",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # ⭐ NEW: Users can star/favorite ideas
    starred_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="starred_ideas",
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    # Helper properties
    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_comments(self):
        return self.comments.count()

    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.score for r in ratings) / ratings.count(), 1)
        return 0

    @property
    def total_stars(self):
        return self.starred_by.count()

    def is_starred_by(self, user):
        return self.starred_by.filter(id=user.id).exists()


# -------------------------
# Like Model
# -------------------------
class Like(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('idea', 'user')


# -------------------------
# Comment Model
# -------------------------
class Comment(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# -------------------------
# Report Model
# -------------------------
class Report(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('idea', 'user')  # one report per user per idea


# -------------------------
# Rating Model
# -------------------------
class Rating(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=1)  # 1–5

    class Meta:
        unique_together = ("idea", "user")

    def __str__(self):
        return f"{self.score} by {self.user} on {self.idea}"


# -------------------------
# Translation Model
# -------------------------
class Translation(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="translations")
    language_code = models.CharField(max_length=10)  # e.g. 'hi', 'ta', 'ml'
    title_translated = models.CharField(max_length=200)
    description_translated = models.TextField()

    class Meta:
        unique_together = ("idea", "language_code")

    def __str__(self):
        return f"{self.idea.title} ({self.language_code})"


# -------------------------
# Newsletter Subscriber
# -------------------------
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
