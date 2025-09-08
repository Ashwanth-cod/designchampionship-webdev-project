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


# -------------------------
# Contact Message Model
# -------------------------
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Contact message from {self.name}'


# -------------------------
# Messaging Models (Email-like)
# -------------------------
class Conversation(models.Model):
    subject = models.CharField(max_length=255, default="(No Subject)")
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversations_as_user1"
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversations_as_user2"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conversation"
        unique_together = (("user1", "user2"),)

    def save(self, *args, **kwargs):
        # Ensure consistent ordering of participants
        if self.user1.id > self.user2.id:
            self.user1, self.user2 = self.user2, self.user1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject} ({self.user1.username} & {self.user2.username})"


class Message(models.Model):
    FOLDER_CHOICES = [
        ("inbox", "Inbox")
    ]

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject_override = models.CharField(max_length=255, blank=True)  # e.g. "Re: ..."
    text = models.TextField(blank=True)
    attachment = models.FileField(upload_to="message_attachments/", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_reported = models.BooleanField(default=False)
    folder = models.CharField(max_length=20, choices=FOLDER_CHOICES, default="inbox")

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.subject_override or self.conversation.subject} from {self.sender.username}"

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def mark_as_unread(self):
        self.is_read = False
        self.save()

    def reply(self, user, text, subject=None):
        """Reply to this message in the same conversation."""
        if self.sender == user:
            return None
        return Message.objects.create(
            conversation=self.conversation,
            sender=user,
            text=text,
            subject_override=subject or f"Re: {self.subject_override or self.conversation.subject}",
            folder="sent"
        )

class MessageReport(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="reports")
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.reported_by} on message {self.message.id}"
