import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Idea, ContactMessage, Message, MessageReport

# -------------------------
# Signup Form
# -------------------------
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
        # Optional validation for phone number format
        if not re.match(r'^\+?\d{10,15}$', phone_number):
            raise forms.ValidationError("Invalid phone number format. It should be 10-15 digits.")
        return phone_number


# -------------------------
# User Update Form
# -------------------------
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'dob', 'phone_number', 'school_name', 'is_student']


# -------------------------
# Idea Form
# -------------------------
class IdeaForm(forms.ModelForm):
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

    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your idea title', 'class': 'form-control'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Describe your idea...', 'class': 'form-control', 'rows': 7, 'style': 'white-space: pre-wrap;'})
    )
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Idea
        fields = ['title', 'description', 'category', 'image', 'document']


# -------------------------
# Login Form (with placeholders)
# -------------------------
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username', 'autofocus': 'autofocus'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )


# -------------------------
# Contact Form
# -------------------------
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


# -------------------------
# Messaging Forms
# -------------------------

# Form for sending a message
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Type your message here...',
                'rows': 3
            })
        }

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text.strip()) == 0:
            raise forms.ValidationError("Message cannot be empty.")
        return text


# Form for reporting a message
class MessageReportForm(forms.ModelForm):
    class Meta:
        model = MessageReport
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Optional reason for reporting this message...',
                'rows': 3
            })
        }

    def clean_reason(self):
        reason = self.cleaned_data.get('reason')
        if len(reason.strip()) == 0:
            raise forms.ValidationError("Reason for reporting cannot be empty.")
        return reason
