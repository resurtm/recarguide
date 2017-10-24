from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from recarguide.auth.forms import UserCreationForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password1'))
            login(request, user)
            # change to home page or something else
            return redirect('auth:login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
