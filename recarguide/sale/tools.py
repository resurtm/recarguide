import datetime
from email.utils import parseaddr

from django.shortcuts import redirect

from recarguide.sale.models import SellProcess


def ensure_sell_process(step):
    def dec1(func):
        def dec2(request, *args, **kwargs):
            try:
                sp = SellProcess.objects.filter(user_id=request.user.id,
                                                finished=False).get()
            except SellProcess.DoesNotExist:
                sp = SellProcess(user_id=request.user.id)
                sp.save()
            if sp.step < step:
                return redirect('sale:step{}'.format(sp.step))
            return func(request, sp, *args, **kwargs)

        return dec2

    return dec1


def assert_stripe_data(func):
    def dec(request, *args, **kwargs):
        if request.method == 'POST':
            assert request.POST['stripeTokenType'] == 'card'
            assert '@' in parseaddr(request.POST['stripeEmail'])[1]
            assert request.POST['stripeToken'].startswith('tok_')
        return func(request, *args, **kwargs)

    return dec


def years_choices(include_empty=True, min_year=1900, max_year=None):
    """
    Generates list containing tuples of years. The first element of tuple must
    be used as a value for the <option></option> HTML tag, and the second one
    must be used as a text/label for the same tag. To be used with the
    <select></select> tag.

    :param include_empty: whether empty choice must included in the final
        choices list
    :type include_empty: bool

    :param min_year: minimal/lowest year of the generated range, the default
        value is 1900
    :type min_year: int

    :param max_year: minimal/lowest year of the generated range, the default
        value is the current year
    :type max_year: int

    :return: returns choices list for the HTML <option></option> tags,
        to be used with the <select></select> tag
    :rtype: list[(int, str)]
    """
    if max_year is None:
        max_year = datetime.datetime.now().year
    choices = [(i, str(i)) for i in range(max_year, min_year - 1, -1)]
    if include_empty:
        choices.insert(0, (None, ''))
    return choices
