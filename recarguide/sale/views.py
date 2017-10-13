from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from recarguide.sale.models import PackagePlan


@login_required
def sale(request):
    return redirect('sale:step1')


@login_required
def step1(request):
    plans = PackagePlan.objects.order_by('order').all()
    return render(request, 'sale/step1.html', {'plans': plans})
