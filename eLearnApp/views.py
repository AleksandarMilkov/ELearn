from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect("home")  # Redirect to the homepage or dashboard
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "login.html"


def home_view(request):
    return render(request, 'base.html')