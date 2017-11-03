import base64
import os

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_http_methods, require_GET, \
    require_POST

from recarguide.cars.models import Model, Category, Photo
from recarguide.common.tools import ensure_stripe_api_key
from recarguide.sale.forms import CarSaleForm, SaleContactForm
from recarguide.sale.models import PackagePlan
from recarguide.sale.tasks import process_photo
from recarguide.sale.tools import ensure_sell_process, assert_stripe_data


@login_required
@require_GET
def sale(request):
    return redirect('sale:step1')


@login_required
@require_http_methods(['GET', 'POST'])
@ensure_sell_process(step=1)
def step1(request, process):
    if request.method == 'POST':
        if not process.package_plan:
            try:
                plan_id = request.POST.get('package_plan_id', '0')
                process.package_plan = PackagePlan.objects.get(id=int(plan_id))
            except:
                raise SuspiciousOperation('Cannot find the package plan')
        process.step = process.step if process.step > 2 else 2
        process.save()
        return redirect('sale:step2')
    plans = PackagePlan.objects.order_by('order').all()
    return render(request, 'sale/step1.html', {'plans': plans,
                                               'process': process})


@login_required
@require_http_methods(['GET', 'POST'])
@ensure_sell_process(step=2)
def step2(request, process):
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
    return render(request, 'sale/step2.html', {'form': form, 'photos': photos})


@login_required
@require_http_methods(['GET', 'POST'])
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
@require_http_methods(['GET', 'POST'])
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
@require_http_methods(['GET', 'POST'])
@ensure_sell_process(step=5)
def step5(request, process):
    if request.method == 'POST' and request.POST.get('confirm') == 'yes':
        process.publish()
        return redirect('cars:view', slug=process.car.slug, id=process.car.id)
    return render(request, 'sale/step5.html')


@login_required
@require_GET
def fetch_models(request, make_id):
    return JsonResponse({m.pk: m.name
                         for m in Model.objects.filter(make_id=make_id)})


@login_required
@require_GET
def fetch_categories(request, category_id):
    r = {c.pk: c.name for c in Category.objects.filter(parent_id=category_id)}
    return JsonResponse(r)


@login_required
@require_POST
@ensure_sell_process(step=2)
def upload_photo(request, process):
    if 'photo' not in request.FILES:
        return HttpResponse('')
    uid, file = get_random_string(16), request.FILES['photo']
    path = os.path.join(settings.MEDIA_ROOT,
                        FileSystemStorage().save(uid, file))
    with open(path, 'rb') as fp:
        data = fp.read()
    os.remove(path)
    photo = Photo(sell_process=process, uid=uid, filename=file.name,
                  filedata=base64.standard_b64encode(data),
                  user=request.user)
    photo.save()
    process_photo.delay(photo.id)
    return HttpResponse(photo.id)


@login_required
@require_POST
def delete_photo(request):
    photo = Photo.objects.filter(pk=int(request.POST.get('id', '0')),
                                 user=request.user)
    photo.delete()
    return HttpResponse('')
