from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.save()
            login(request, user)  # Auto-login after registration
            return redirect('home')  # Change 'home' to your actual home page URL name
    else:
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

def home_view(request):
    return render(request, "base.html")