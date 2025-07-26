from django.shortcuts import render, redirect, HttpResponse
from users.forms import RegistrationForm, LoginForm, CreateGroupForm, ProfileUpdateForm, CustomPasswordChangeForm,CustomPasswordResetForm, CustomPasswordResetConfirmForm
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy

User = get_user_model()

# Create your views here.

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = "accounts/edit-profile.html"
    context_object_name = "form"

    def get_object(self):
        return self.request.user
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your profile has been updated successfully.")
        return redirect("users:edit-profile")
    
class ChangePassword(LoginRequiredMixin, PasswordChangeView):
    template_name = "accounts/password-change.html"
    success_url = reverse_lazy("users:password-change-done")
    form_class = CustomPasswordChangeForm

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = "registration/reset-password.html"
    email_template_name = "registration/reset-email.html"
    success_url = reverse_lazy("users:sign-in")

    def form_valid(self, form):
        self.extra_email_context = {
            "protocol": 'https' if self.request.is_secure() else "http",
            "domain": self.request.get_host(),
        }
        messages.success(self.request, "A reset email has been sent. Please check your email.")
        return super().form_valid(form)

class CustomPassowrdResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = "registration/reset-password.html"
    success_url = reverse_lazy("users:sign-in")

    def form_valid(self, form):
        messages.success(self.request, "Password reset successfull.")
        return super().form_valid(form)


def sign_up(request):
    form = RegistrationForm()
    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(request, "Please check your mail to activate account.")
            return redirect("users:sign-in")
    
    return render(request, "sign-up.html", {"form": form})


def sign_in(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")

    return render(request, "sign-in.html", {"form": form})

@login_required
def sign_out(request):
    logout(request)
    return redirect("users:sign-in")


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("users:sign-in")
        else:
            return HttpResponse("Invalid id or token.")

    except User.DoesNotExist:
        return HttpResponse("User doesn't exists.")
    


class ProfileView(TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["username"] = user.username
        context["email"] = user.email
        context["name"] = user.get_full_name()
        context["profile_picture"] = user.profile_picture
        context["phone_number"] = user.phone_number
        context["member_since"] = user.date_joined
        context["last_login"] = user.last_login

        return context
    


