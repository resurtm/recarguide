from django.shortcuts import render

from recarguide.auth.forms import UserCreationForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
