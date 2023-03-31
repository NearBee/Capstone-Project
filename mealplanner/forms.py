from django import forms
from django.forms import (
    TextInput,
    EmailInput,
    PasswordInput,
    Select,
    CheckboxInput,
    ClearableFileInput,
)

from .models import User, Planner


class user_registration_form(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
        )
        exclude = ("profile_picture",)
        widgets = {
            "username": TextInput(
                attrs={
                    "class": "form-control mb-4 shadow-sm forminputBox",
                }
            ),
            "email": EmailInput(
                attrs={
                    "class": "form-control mb-4 shadow-sm forminputBox",
                }
            ),
            "password": PasswordInput(
                attrs={
                    "class": "form-control mb-4 shadow-sm forminputBox",
                }
            ),
        }
        labels = {
            "username": "Username",
            "email": "Email",
            "password": "Password",
        }


class user_edit_form(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "profile_picture",
            "username",
            "email",
        )
        exclude = ("password",)
        widgets = {
            "profile_picture": ClearableFileInput(
                attrs={
                    "class": "form-control shadow-sm mb-1 forminputBox",
                }
            ),
            "username": TextInput(
                attrs={
                    "class": "form-control shadow-sm mb-1 forminputBox",
                }
            ),
            "email": EmailInput(
                attrs={
                    "class": "form-control shadow-sm mb-1 forminputBox",
                }
            ),
        }
        labels = {
            "profile_picture": "New Profile Picture",
            "username": "New Username",
            "email": "New Email",
        }


class user_login_form(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )
        widgets = {
            "username": TextInput(
                attrs={
                    "class": "form-control mb-4 shadow-sm forminputBox",
                }
            ),
            "password": PasswordInput(
                attrs={
                    "class": "form-control mb-4 shadow-sm forminputBox",
                }
            ),
        }
        labels = {
            "username": "Username",
            "password": "Password",
        }


class planner_creation_form(forms.ModelForm):
    class Meta:
        model = Planner
        field = (
            "name",
            "days",
        )
        exclude = (
            "owner",
            "chosen_list",
            "not_saveable",
            "finished",
            "likes",
            "created_at",
            "is_private",
        )
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control mb-4 me-5 shadow-sm forminputBox",
                    "placeholder": "Planner name here!",
                }
            ),
            "days": Select(
                attrs={"class": "form-select mb-4 me-5 shadow-sm form-select-sm"}
            ),
        }
        labels = {
            "name": "Planner name:",
            "days": "How many days in this planner?",
        }
