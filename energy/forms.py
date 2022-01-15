from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.forms import ModelForm, NumberInput, DateInput, Select, ModelChoiceField

from .models import Register


class PlanningCreateForm(forms.Form):
    local = NumberInput()
    reading_day = forms.DateField(help_text='Seleccione día (1) del mes', label='Fecha',
                                  widget=DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    plan_lv = forms.IntegerField(required=True, min_value=0, label='Plan de lunes a viernes',
                                 widget=NumberInput(attrs={'class': 'form-control'}))
    plan_sd = forms.IntegerField(required=True, min_value=0, label='Plan de sabado y domingo',
                                 widget=NumberInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        local = kwargs.pop('local')
        super().__init__(*args, **kwargs)
        self.fields['local'] = ModelChoiceField(queryset=local, widget=Select(attrs={'class': 'form-select'}))

    def clean(self):
        cleaned_data = super().clean()
        reading_day = cleaned_data.get('reading_day')
        local = cleaned_data.get('local')
        try:
            if Register.objects.get(reading_day=reading_day, local=local):
                raise ValidationError("%s ya tiene registro en este mes" % local)
        except ObjectDoesNotExist:
            pass


class RegisterUpdateForm(ModelForm):
    class Meta:
        model = Register
        fields = ['plan', 'reading']
        widgets = {
            'plan': NumberInput(attrs={'class': 'form-control'}),
            'reading': NumberInput(attrs={'class': 'form-control'}),
        }
