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
    is_active = models.BooleanField(default=True)

    @property
    def age(self):
        from datetime import date
        if self.dob:
            today = date.today()
            return today.year - self.dob.year - (
                (today.month, today.day) < (self.dob.month, self.dob.day)
            )
        return None

    @property
    def followers_list(self):
        return self.followers.all()

    @property
    def following_list(self):
        return self.following.all()

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    def __str__(self):
        return self.username


# -------------------------
# Follow Model
# -------------------------
class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower} follows {self.following}"


# -------------------------
# Idea Model
# -------------------------
class Idea(models.Model):
    CATEGORY_CHOICES = [
        ("tech", "Technology"),
        ("edu", "Education"),
        ("art", "Art & Creativity"),
        ("science", "Science"),
        ("business", "Business & Entrepreneurship"),
        ("health", "Health & Wellness"),
        ("gaming", "Gaming"),
        ("social", "Social Impact"),
        ("entertainment", "Entertainment"),
        ("sports", "Sports & Fitness"),
        ("travel", "Travel & Lifestyle"),
        ("other", "Other"),
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

    starred_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="starred_ideas",
        blank=True,
    )

    is_archived = models.BooleanField(default=False)

    image = models.ImageField(upload_to="idea_images/", blank=True, null=True)
    document = models.FileField(upload_to="idea_documents/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

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
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("idea", "user")

# -------------------------
# Comment Model
# -------------------------
class Comment(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Contact message from {self.name}'
