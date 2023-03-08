from django import forms
from django.forms import TextInput, EmailInput, PasswordInput, Select, CheckboxInput

from .models import User, Planner


class user_registration_form(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
        )
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
            "is_private",
        )
        exclude = (
            "owner",
            "chosen_list",
            "not_saveable",
        )
        widgets = {
            "name": TextInput(attrs={"class": "form control"}),
            "days": Select(attrs={"class": "form-select form-select-sm"}),
            "is_private": CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "name": "Planner name:",
            "days": "How many days?",
            "is_private": "Will this plan be private?",
        }
