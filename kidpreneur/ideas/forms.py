from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Idea, Subscriber

# -------------------------
# Signup Form
# -------------------------
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser




class CustomUserCreationForm(UserCreationForm):
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), required=True
    )
    is_student = forms.BooleanField(required=False)
    school_name = forms.CharField(required=False)
    phone_number = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "dob",
            "is_student",
            "school_name",
            "phone_number",
            "email",
            "username",
            "password1",
            "password2",
        ]

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']

# -------------------------
# Idea Form
# -------------------------
class IdeaForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('tech', 'Technology'),
        ('art', 'Art'),
        ('education', 'Education'),
        ('science', 'Science'),
        ('business', 'Business'),
        ('other', 'Other'),
    ]

    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your idea title',
            'class': 'form-control'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Describe your idea...',
            'class': 'form-control',
            'rows': 5
        })
    )
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Idea
        fields = ['title', 'description', 'category']

# -------------------------
# Newsletter Form
# -------------------------
class SubscriberForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Subscriber
        fields = ['email']
