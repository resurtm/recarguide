from django.shortcuts import render, redirect

from auth.forms import UserCreationForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('common:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
