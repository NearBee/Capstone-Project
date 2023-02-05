from django import forms
from django.forms import TextInput, EmailInput, PasswordInput

from .models import User


class user_creation_form(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "password_confirmation",
        )
        widgets = {
            "username": TextInput(
                attrs={
                    "class": "form-control my-2",
                }
            ),
            "email": EmailInput(
                attrs={
                    "class": "form-control my-2",
                }
            ),
            "password": PasswordInput(
                attrs={
                    "class": "form-control my-2",
                }
            ),
            "password_confirmation": PasswordInput(
                attrs={
                    "class": "form-control my-2",
                }
            ),
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
                    "class": "form-control my-2",
                }
            ),
            "password": PasswordInput(
                attrs={
                    "class": "form-control my-2",
                }
            ),
        }
