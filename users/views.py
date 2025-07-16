from django.shortcuts import render, redirect, HttpResponse
from users.forms import RegistrationForm, LoginForm, CreateGroupForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.

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
    


