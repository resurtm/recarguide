from django.forms import ModelForm, ModelChoiceField, ChoiceField

from recarguide.cars.models import Car, Make, Model, Category
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
        fields = ['price', 'mileage', 'description']
        labels = {
            'make': 'Make/Manufacturer',
        }

    def __init__(self, *args, **kwargs):
        super(CarSaleForm, self).__init__(*args, **kwargs)

        if 'make' in self.data and len(self.data['make']) > 0:
            qs = Model.objects.filter(make_id=int(self.data['make']))
            choices = [(m.pk, m.name) for m in qs]
            if len(choices) > 0:
                choices.insert(0, (None, ''))
            self.fields['model'].choices = choices
            self.fields['model'].queryset = qs

        if 'category' in self.data and len(self.data['category']) > 0:
            qs = Category.objects.filter(parent_id=int(self.data['category']))
            choices = [(c.pk, c.name) for c in qs]
            if len(choices) > 0:
                choices.insert(0, (None, ''))
            self.fields['subcategory'].choices = choices
            self.fields['subcategory'].queryset = qs
        if len(self.fields['subcategory'].choices) == 0:
            self.fields['subcategory'].required = False

    def save(self, *args, **kwargs):
        self.instance.year = int(self.cleaned_data['year'])
        self.instance.make = self.cleaned_data['make']
        self.instance.model = self.cleaned_data['model']
        if 'subcategory' in self.cleaned_data:
            self.instance.category = self.cleaned_data['subcategory']
        else:
            self.instance.category = self.cleaned_data['category']
        return super(CarSaleForm, self).save(*args, **kwargs)
