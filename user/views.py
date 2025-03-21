from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def register(request):
    form = CustomUserForm()

    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('user:login')
    context = {'form': form}
    return render(request, 'register.html', context)

def user_login(request): 
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return HttpResponseRedirect(reverse("admin:index"))
            else:
                return HttpResponseRedirect(reverse("user:success"))
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def user_logout(request):
    logout(request)
    response = HttpResponseRedirect(reverse('user:login'))
    return response

@login_required(login_url='/login')
def show_success(request):
    return render(request, 'success.html')