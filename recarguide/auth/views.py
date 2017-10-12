from django.shortcuts import render

from recarguide.auth.forms import UserCreationForm


def signup(request):
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
