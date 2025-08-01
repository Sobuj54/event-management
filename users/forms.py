from django import forms
from django.contrib.auth.models import  Permission, Group
from participant.forms import ParticipantFormMixin
import re
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationForm( ParticipantFormMixin ,forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password"]

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            if not re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])(?=.{8,})', password):
                raise forms.ValidationError( "Password must be at least 8 characters long and contain at least one uppercase letter, "
                    "one lowercase letter, one digit, and one special character.")
            
        return password
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password",_("Passwords do not match"))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit==True:
            user.save()
        
        return user
    

class LoginForm(ParticipantFormMixin, AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class CreateGroupForm(ParticipantFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign permissions"
    )

    class Meta:
        model = Group
        fields = ["name", "permissions"]


class ProfileUpdateForm(ParticipantFormMixin, forms.ModelForm):
    class Meta: 
        model = User
        fields = ["email", "first_name", "last_name", "phone_number", "profile_picture"]


class CustomPasswordChangeForm(ParticipantFormMixin, PasswordChangeForm):
    pass

class CustomPasswordResetForm(ParticipantFormMixin, PasswordResetForm):
    pass

class CustomPasswordResetConfirmForm(ParticipantFormMixin, SetPasswordForm):
    pass

