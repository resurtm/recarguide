import base64
import os

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string

from recarguide.cars.models import Model, Category, Photo
from recarguide.common.tools import ensure_stripe_api_key
from recarguide.sale.forms import CarSaleForm, SaleContactForm
from recarguide.sale.models import PackagePlan
from recarguide.sale.tasks import process_photo
from recarguide.sale.tools import ensure_sell_process, assert_stripe_data


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
        process.step = process.step if process.step > 2 else 2
        process.save()
        return redirect('sale:step2')
    plans = PackagePlan.objects.order_by('order').all()
    return render(request, 'sale/step1.html', {'plans': plans,
                                               'process': process})


@login_required
@ensure_sell_process(step=2)
def step2(request, process):
    # raise SuspiciousOperation('Invalid package plan has been specified')
    if request.method == 'POST':
        form = CarSaleForm(request.POST, instance=process.car)
        if form.is_valid():
            with transaction.atomic():
                process.car = form.save()
                process.step = process.step if process.step > 3 else 3
                process.save()
            return redirect('sale:step3')
    else:
        form = CarSaleForm(instance=process.car)
    photos = Photo.objects.filter(sell_process=process)
    return render(request, 'sale/step2.html', {'form': form,
                                               'photos': photos})


@login_required
@ensure_sell_process(step=3)
def step3(request, process):
    if request.method == 'POST':
        form = SaleContactForm(request.POST, instance=process.contacts.first())
        if form.is_valid():
            with transaction.atomic():
                form.instance.sell_process = process
                form.save()
                process.step = process.step if process.step > 4 else 4
                process.save()
            return redirect('sale:step4')
    else:
        form = SaleContactForm(instance=process.contacts.first())
    return render(request, 'sale/step3.html', {'form': form})


@login_required
@ensure_sell_process(step=4)
@assert_stripe_data
def step4(request, process):
    ensure_stripe_api_key()
    if request.method == 'POST':
        resp = stripe.Charge.create(
            amount=process.package_plan.stripe_price,
            currency='usd',
            card=request.POST['stripeToken'],
            description='SELL_PROCESS_ID={}'.format(process.id),
        )
        process.payment = resp
        process.step = 5
        process.save()
        return redirect('sale:step4')
    return render(request, 'sale/step4.html', {'process': process})


@login_required
@ensure_sell_process(step=5)
def step5(request, process):
    process.finished = True
    process.save()
    return render(request, 'sale/step5.html')


@login_required
def fetch_models(request, make_id):
    models = Model.objects.filter(make_id=make_id)
    result = {}
    for model in models:
        result[model.pk] = model.name
    return JsonResponse(result)


@login_required
def fetch_categories(request, category_id):
    models = Category.objects.filter(parent_id=category_id)
    result = {}
    for model in models:
        result[model.pk] = model.name
    return JsonResponse(result)


@login_required
@ensure_sell_process(step=2)
def photos_upload(request, process):
    if request.method == 'POST' and 'photos' in request.FILES:
        file = request.FILES['photos']
        uid = get_random_string(16)
        filename = FileSystemStorage().save(uid, file)
        filepath = os.path.join(settings.MEDIA_ROOT, filename)
        with open(filepath, 'rb') as fp:
            filedata = fp.read()
        os.remove(filepath)
        photo = Photo(sell_process=process,
                      uid=uid,
                      filename=file.name,
                      filedata=base64.standard_b64encode(filedata))
        photo.save()
        process_photo.delay(photo.id)
    return JsonResponse({})
