from django import forms
from django.forms import CharField, EmailField

from .models import User


class user_creation_form(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
        )
        # widgets = {
        #     "username": CharField(
        #         required=True,
        #         min_length=1,
        #         max_length=15,
        #         strip=True,
        #     ),
        #     "email": EmailField(
        #         required=True,
        #     ),
        #     "password": CharField(
        #         required=True, min_length=1, max_length=127, strip=True
        #     ),
        # }


class user_login_form(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )
        # widgets = {
        #     "username": CharField(
        #         required=True, min_length=1, max_length=15, strip=True
        #     ),
        #     "password": CharField(
        #         required=True, min_length=1, max_length=127, strip=True
        #     ),
        # }
