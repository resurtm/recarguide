import datetime

from django.shortcuts import redirect

from recarguide.sale.models import SellProcess


def ensure_sell_process(step):
    def dec1(func):
        def dec2(request, *args, **kwargs):
            sp, __ = SellProcess.objects.get_or_create(user_id=request.user.id)
            if sp.step != step:
                return redirect('sale:step{}'.format(sp.step))
            return func(request, sp, *args, **kwargs)

        return dec2

    return dec1


def years_choices(include_empty=True):
    year = datetime.datetime.now().year
    choices = [(i, i) for i in range(year, 1900, -1)]
    if include_empty:
        choices.insert(0, (None, ''))
    return choices
