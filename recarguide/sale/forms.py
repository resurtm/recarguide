from django.forms import ModelForm, ModelChoiceField

from recarguide.cars.models import Car, Make, Model


class CarSaleForm(ModelForm):
    make = ModelChoiceField(queryset=Make.objects.all(), to_field_name='id',
                            empty_label='')
    model = ModelChoiceField(queryset=Model.objects.none(), to_field_name='id',
                             empty_label='')

    class Meta:
        model = Car
        fields = ['make', 'model', 'price', 'year', 'mileage', 'description']
        labels = {
            'make': 'Make/Manufacturer',
        }
