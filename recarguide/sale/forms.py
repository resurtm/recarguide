from django.forms import ModelForm, ModelChoiceField, ChoiceField

from recarguide.cars.models import Car, Make, Model, Category
from recarguide.common.countries import get_countries
from recarguide.sale.models import Contact
from recarguide.sale.utils import years_choices


class CarSaleForm(ModelForm):
    year = ChoiceField(choices=years_choices())

    make = ModelChoiceField(queryset=Make.objects.order_by('name'),
                            to_field_name='id',
                            empty_label='')
    model = ModelChoiceField(queryset=Model.objects.none(),
                             to_field_name='id',
                             empty_label='')

    category = ModelChoiceField(
        queryset=Category.objects.filter(parent__isnull=True).order_by('name'),
        to_field_name='id',
        empty_label='')
    subcategory = ModelChoiceField(
        queryset=Category.objects.none(),
        to_field_name='id',
        empty_label='')

    class Meta:
        model = Car
        fields = ['year', 'price', 'mileage', 'description']
        labels = {
            'make': 'Make/Manufacturer',
        }

    def __init__(self, *args, **kwargs):
        super(CarSaleForm, self).__init__(*args, **kwargs)

        if len(self.data) == 0:
            self.__setup_model_field(self.instance.make.id)
            self.fields['make'].initial = self.instance.make
            self.fields['model'].initial = self.instance.model
            if self.instance.category.parent is None:
                self.fields['category'].initial = self.instance.category
                self.fields['subcategory'].initial = None
            else:
                self.__setup_subcategory_field(self.instance.category.parent.id)
                self.fields['category'].initial = self.instance.category.parent
                self.fields['subcategory'].initial = self.instance.category

        if 'make' in self.data and len(self.data['make']) > 0:
            self.__setup_model_field(int(self.data['make']))
        if 'category' in self.data and len(self.data['category']) > 0:
            self.__setup_subcategory_field(int(self.data['category']))
        if len(self.fields['subcategory'].choices) == 0:
            self.fields['subcategory'].required = False

    def save(self, *args, **kwargs):
        self.instance.year = int(self.cleaned_data['year'])
        self.instance.make = self.cleaned_data['make']
        self.instance.model = self.cleaned_data['model']
        if self.cleaned_data['subcategory'] is None:
            self.instance.category = self.cleaned_data['category']
        else:
            self.instance.category = self.cleaned_data['subcategory']
        return super(CarSaleForm, self).save(*args, **kwargs)

    def __setup_model_field(self, make):
        qs = Model.objects.filter(make_id=make)
        choices = [(m.pk, m.name) for m in qs]
        if len(choices) > 0:
            choices.insert(0, (None, ''))
        self.fields['model'].choices = choices
        self.fields['model'].queryset = qs

    def __setup_subcategory_field(self, category):
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
        labels = {
            'address2': 'Address (additional)',
            'contact_method': 'Contact Method',
        }

    def __init__(self, *args, **kwargs):
        super(SaleContactForm, self).__init__(*args, **kwargs)
        if len(self.data) == 0:
            self.fields['country'].initial = self.instance.country
        self.fields['address2'].required = False

    def save(self, *args, **kwargs):
        self.instance.country = self.cleaned_data['country']
        return super(SaleContactForm, self).save(*args, **kwargs)
