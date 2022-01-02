from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()

class RegisterSeller(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "email", "password", "phone_number",]

        widgets = {"password": (forms.PasswordInput)}

        labels = {
            "username": ("username"),
            "password": ("password"),
            "email": ("email"),
            "phone_number": ("phone_number"),
        }

        def clean_repeat_password(self):
            repeat_password = self.cleaned_data["repeat_password"]
            new_password = self.cleaned_data["new_password"]
            if new_password != repeat_password:
                raise ValidationError("password and repeat password must be same")
            return repeat_password