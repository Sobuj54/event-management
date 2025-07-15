from django.shortcuts import render, redirect
from users.forms import RegistrationForm

# Create your views here.
def sign_up(request):
    form = RegistrationForm()
    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        return redirect("sign-up")
    
    return render(request, "sign-up.html", {"form": form})