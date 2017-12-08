from django.shortcuts import render


def index(request):
    return render(request, 'cars/index.html')
