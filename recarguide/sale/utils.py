from django.shortcuts import redirect

from recarguide.sale.models import SellProcess


def ensure_sell_process(step=None):
    assert step is not None

    def dec1(func):
        def dec2(request):
            sp, __ = SellProcess.objects.get_or_create(user_id=request.user.id)
            if sp.step != step:
                return redirect('sale:step{}'.format(sp.step))
            return func(request, sp)

        return dec2

    return dec1
