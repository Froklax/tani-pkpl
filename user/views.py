from django.shortcuts import render
from django.contrib import messages
from .forms import CustomUserForm

def register(request):
    form = CustomUserForm()

    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return render(request, 'success.html')
    context = {'form': form}
    return render(request, 'register.html', context)

def show_success(request):
    return render(request, 'success.html')