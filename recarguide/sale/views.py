from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse
from django.shortcuts import render, redirect

from recarguide.cars.models import Model, Category
from recarguide.sale.forms import CarSaleForm
from recarguide.sale.models import PackagePlan
from recarguide.sale.utils import ensure_sell_process


@login_required
def sale(request):
    return redirect('sale:step1')


@login_required
@ensure_sell_process(step=1)
def step1(request, process):
    if request.method == 'POST':
        plan_id = request.POST.get('package_plan_id', '').strip()
        if plan_id == '':
            raise SuspiciousOperation('Invalid package plan has been specified')

        process.package_plan = PackagePlan.objects.get(id=int(plan_id))
        process.step = 2
        process.save()

        return redirect('sale:step2')

    plans = PackagePlan.objects.order_by('order').all()
    return render(request, 'sale/step1.html', {'plans': plans})


@login_required
@ensure_sell_process(step=2)
def step2(request, process):
    if request.method == 'POST':
        form = CarSaleForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = CarSaleForm()
    return render(request, 'sale/step2.html', {'form': form})


@login_required
@ensure_sell_process(step=2)
def fetch_models(request, process, make_id):
    models = Model.objects.filter(make_id=make_id)
    result = {}
    for model in models:
        result[model.pk] = model.name
    return JsonResponse(result)


@login_required
@ensure_sell_process(step=2)
def fetch_categories(request, process, category_id):
    models = Category.objects.filter(parent_id=category_id)
    result = {}
    for model in models:
        result[model.pk] = model.name
    return JsonResponse(result)
