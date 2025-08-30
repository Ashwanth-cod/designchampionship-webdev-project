from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Idea


# --- User Signup Form ---
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Email address"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add bootstrap classes + placeholders
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            if not field.widget.attrs.get("placeholder"):
                field.widget.attrs["placeholder"] = field.label


# --- Idea Submission Form ---
class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ["name", "logo", "description", "category"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap + placeholders
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

            if field_name == "logo":
                field.widget.attrs["class"] = "form-control-file"
            else:
                field.widget.attrs["placeholder"] = field.label