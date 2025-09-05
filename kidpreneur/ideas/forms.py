from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Idea

# -------------------------
# Signup Form
# -------------------------
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
        fields = ['username', 'email', 'first_name', 'last_name', 'dob', 'phone_number', 'school_name', 'is_student']


# -------------------------
# Idea Form
# -------------------------
class IdeaForm(forms.ModelForm):
    # Expanded list of categories
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
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your idea title',
            'class': 'form-control'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Describe your idea...',
            'class': 'form-control',
            'rows': 7,             # taller textarea
            'style': 'white-space: pre-wrap;'  # preserves line breaks and tabs
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
