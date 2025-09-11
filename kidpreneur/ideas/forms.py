import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import (
    CustomUser, Idea, ContactMessage, Message, MessageReport,
    ForumPost, ForumPostComment, ForumPostReport
)

class CustomUserCreationForm(UserCreationForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    is_student = forms.BooleanField(required=False)
    school_name = forms.CharField(required=False)
    phone_number = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = [
            "first_name", "last_name", "dob", "is_student", "school_name", "phone_number",
            "email", "username", "password1", "password2"
        ]

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r'^\+?\d{10,15}$', phone_number):
            raise forms.ValidationError("Invalid phone number format. It should be 10–15 digits.")
        return phone_number

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'dob', 'phone_number', 'school_name', 'is_student']

class IdeaForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('tech', 'Technology'), ('edu', 'Education'), ('art', 'Art & Creativity'),
        ('science', 'Science'), ('business', 'Business & Entrepreneurship'),
        ('health', 'Health & Wellness'), ('gaming', 'Gaming'), ('social', 'Social Impact'),
        ('entertainment', 'Entertainment'), ('sports', 'Sports & Fitness'),
        ('travel', 'Travel & Lifestyle'), ('other', 'Other'),
    ]

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your idea title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Describe your idea...', 'rows': 7}))
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

    class Meta:
        model = Idea
        fields = ['title', 'description', 'category', 'image', 'document']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        slug = '-'.join(''.join(c if c.isalnum() or c == ' ' else '' for c in title.lower()).split())
        self.instance.slug = slug
        return title

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email address'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject of your message'}),
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Type your message here...'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message here...'})
        }

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text.strip()) == 0:
            raise forms.ValidationError("Message cannot be empty.")
        return text

class MessageReportForm(forms.ModelForm):
    class Meta:
        model = MessageReport
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional reason for reporting this message...'})
        }

    def clean_reason(self):
        reason = self.cleaned_data.get('reason')
        if len(reason.strip()) == 0:
            raise forms.ValidationError("Reason for reporting cannot be empty.")
        return reason

class ForumPostForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('tech', 'Technology'), ('edu', 'Education'), ('art', 'Art & Creativity'),
        ('science', 'Science'), ('business', 'Business & Entrepreneurship'),
        ('health', 'Health & Wellness'), ('gaming', 'Gaming'), ('social', 'Social Impact'),
        ('entertainment', 'Entertainment'), ('sports', 'Sports & Fitness'),
        ('travel', 'Travel & Lifestyle'), ('other', 'Other'),
    ]

    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

    class Meta:
        model = ForumPost
        fields = ['title', 'content', 'category', 'image', 'document']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply common class
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        # Add specific placeholders
        self.fields['title'].widget.attrs.update({
            'placeholder': 'Enter a descriptive title for your post'
        })

        self.fields['content'].widget.attrs.update({
            'placeholder': 'Write the content of your forum post here...'
        })

        self.fields['category'].widget.attrs.update({
            'placeholder': 'Select a category'
        })

        self.fields['image'].widget.attrs.update({
            'placeholder': 'Upload an optional image'
        })

        self.fields['document'].widget.attrs.update({
            'placeholder': 'Upload a document if needed'
        })

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        slug = '-'.join(''.join(c if c.isalnum() or c == ' ' else '' for c in title.lower()).split())
        self.instance.slug = slug

        if ForumPost.objects.filter(slug=slug).exists():
            raise forms.ValidationError("A post with this title already exists. Please use a different title.")

        return title


class ForumPostCommentForm(forms.ModelForm):
    class Meta:
        model = ForumPostComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add your comment...'})
        }

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text.strip()) == 0:
            raise forms.ValidationError("Comment cannot be empty.")
        return text

class ForumPostReportForm(forms.ModelForm):
    class Meta:
        model = ForumPostReport
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Why are you reporting this post?'})
        }

    def clean_reason(self):
        reason = self.cleaned_data.get('reason')
        if len(reason.strip()) == 0:
            raise forms.ValidationError("Please provide a reason for reporting.")
        return reason
