from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm, ModelChoiceField, ChoiceField, CharField

from cars.models import Car, Make, Model, Category
from common.countries import get_countries
from sale.models import Contact
from sale.tools import years_choices


def _rel_or_none(instance, attr):
    try:
        res = getattr(instance, attr)
    except ObjectDoesNotExist:
        res = None
    return res


class CarSaleForm(ModelForm):
    year = ChoiceField(choices=years_choices())

    make = ModelChoiceField(queryset=Make.objects.order_by('name'),
                            to_field_name='id', empty_label='')
    model = ModelChoiceField(queryset=Model.objects.none(),
                             to_field_name='id', empty_label='')

    trim_id = CharField()
    trim_name = CharField()

    category = ModelChoiceField(
        queryset=Category.objects.filter(parent__isnull=True).order_by('name'),
        to_field_name='id', empty_label='')
    subcategory = ModelChoiceField(queryset=Category.objects.none(),
                                   to_field_name='id', empty_label='')

    class Meta:
        model = Car
        fields = ['year', 'price', 'mileage', 'description']
        labels = {'make': 'Make/Manufacturer',
                  'trim_name': 'Trim'}

    def __init__(self, *args, **kwargs):
        super(CarSaleForm, self).__init__(*args, **kwargs)
        self._setup_initial_state()
        if 'make' in self.data and len(self.data['make']) > 0:
            self._setup_model_field(int(self.data['make']))
        self.fields['trim_name'].required = False
        self.fields['trim_id'].required = False
        if 'category' in self.data and len(self.data['category']) > 0:
            self._setup_subcategory_field(int(self.data['category']))
        if len(self.fields['subcategory'].choices) == 0:
            self.fields['subcategory'].required = False

    def save(self, *args, **kwargs):
        self.instance.year = int(self.cleaned_data['year'])
        self.instance.make = self.cleaned_data['make']
        self.instance.model = self.cleaned_data['model']
        self.instance.trim_name = self.cleaned_data['trim_name']
        print(self.cleaned_data)
        try:
            self.instance.trim_id = int(self.cleaned_data['trim_id'])
        except ValueError:
            self.instance.trim_id = None
        if self.cleaned_data['subcategory'] is None:
            self.instance.category = self.cleaned_data['category']
        else:
            self.instance.category = self.cleaned_data['subcategory']
        return super(CarSaleForm, self).save(*args, **kwargs)

    def _setup_initial_state(self):
        if len(self.data) > 0:
            return

        # this is need in order to show empty price & mileage fields in case:
        # 1. sell process is new, 2. form was not submitted
        # without these lines we would have "0" values, not just empty fields
        self.fields['price'].initial = None
        self.fields['mileage'].initial = None

        make = _rel_or_none(self.instance, 'make')
        model = _rel_or_none(self.instance, 'model')
        if make is not None and model is not None:
            self._setup_model_field(make)
            self.fields['make'].initial = make
            self.fields['model'].initial = model

        self.fields['trim_name'].initial = self.instance.trim_name
        self.fields['trim_id'].initial = self.instance.trim_id

        category = _rel_or_none(self.instance, 'category')
        if category is not None:
            if category.parent is None:
                self.fields['category'].initial = category
                self.fields['subcategory'].initial = None
            else:
                self._setup_subcategory_field(category.parent.id)
                self.fields['category'].initial = category.parent
                self.fields['subcategory'].initial = category

    def _setup_model_field(self, make):
        qs = Model.objects.filter(make_id=make)
        choices = [(m.pk, m.name) for m in qs]
        if len(choices) > 0:
            choices.insert(0, (None, ''))
        self.fields['model'].choices = choices
        self.fields['model'].queryset = qs

    def _setup_subcategory_field(self, category):
        qs = Category.objects.filter(parent_id=category)
        choices = [(c.pk, c.name) for c in qs]
        if len(choices) > 0:
            choices.insert(0, (None, ''))
        self.fields['subcategory'].choices = choices
        self.fields['subcategory'].queryset = qs


class SaleContactForm(ModelForm):
    country = ChoiceField(choices=get_countries())

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'address', 'address2', 'city',
                  'phone', 'contact_method', 'zip']
        labels = {'address2': 'Address (additional)',
                  'contact_method': 'Contact Method',
                  'first_name': 'First Name',
                  'last_name': 'Last Name'}

    def __init__(self, *args, **kwargs):
        super(SaleContactForm, self).__init__(*args, **kwargs)
        if len(self.data) == 0:
            self.fields['country'].initial = self.instance.country
        self.fields['address2'].required = False

    def save(self, *args, **kwargs):
        self.instance.country = self.cleaned_data['country']
        return super(SaleContactForm, self).save(*args, **kwargs)
