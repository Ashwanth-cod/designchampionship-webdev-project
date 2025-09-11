from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import ValidationError


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
    description = models.TextField(max_length=2000)
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


class Like(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("idea", "user")

class Comment(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Contact message from {self.name}'

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
        if self.user1.id > self.user2.id:
            self.user1, self.user2 = self.user2, self.user1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject} ({self.user1.username} & {self.user2.username})"

class Message(models.Model):
    class Meta:
        db_table = "ideas_message"

    FOLDER_CHOICES = [
        ("inbox", "Inbox")
    ]

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject_override = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True, max_length=200)
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

class ForumPost(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Technology'),
        ('edu', 'Education'),
        ('art', 'Art & Creativity'),
        ('science', 'Science'),
        ('business', 'Business & Entrepreneurship'),
        ('health', 'Health & Wellness'),
        ('gaming', 'Gaming'),
        ('social', 'Social Impact'),
        ('entertainment', 'Entertainment'),
        ('sports', 'Sports & Fitness'),
        ('travel', 'Travel & Lifestyle'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=255, db_index=True)
    content = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='other')
    image = models.ImageField(upload_to='forum_images/', null=True, blank=True)
    document = models.FileField(upload_to='forum_documents/', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forum_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug_candidate = base_slug
            counter = 1
            while ForumPost.objects.filter(slug=slug_candidate).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)

    def clean(self):
        if not self.title.strip():
            raise ValidationError("Title cannot be empty or whitespace.")
        if not self.content.strip():
            raise ValidationError("Content cannot be empty or whitespace.")

    def __str__(self):
        return f"{self.title} ({self.category})"

    class Meta:
        verbose_name = "Forum Post"
        verbose_name_plural = "Forum Posts"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
        ]

class ForumPostLike(models.Model):
    forum_post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name="forum_post_likes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("forum_post", "user")

    def __str__(self):
        return f"{self.user.username} liked {self.forum_post.title}"

class ForumPostComment(models.Model):
    forum_post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.forum_post.title}"

    @property
    def total_likes(self):
        return self.comment_likes.count()

class ForumPostReport(models.Model):
    forum_post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name="reports")
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.reported_by} on forum post {self.forum_post.title}"
