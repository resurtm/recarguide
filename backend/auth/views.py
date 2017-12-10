from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from auth.forms import UserCreationForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password1'))
            login(request, user)
            return redirect('auth:login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
