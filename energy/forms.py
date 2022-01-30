from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from .models import Register


class PlanningCreateForm(forms.Form):
    local = forms.NumberInput()
    reading_day = forms.DateField(help_text='Seleccione día (1) del mes', label='Fecha',
                                  widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    plan_lv = forms.IntegerField(required=True, min_value=0, label='Plan de lunes a viernes',
                                 widget=forms.NumberInput(attrs={'class': 'form-control'}))
    plan_sd = forms.IntegerField(required=True, min_value=0, label='Plan de sabado y domingo',
                                 widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        local = kwargs.pop('local')
        super().__init__(*args, **kwargs)
        self.fields['local'] = forms.ModelChoiceField(queryset=local,
                                                      widget=forms.Select(attrs={'class': 'form-select'}))

    def clean(self):
        cleaned_data = super().clean()
        reading_day = cleaned_data.get('reading_day')
        local = cleaned_data.get('local')
        try:
            if Register.objects.get(reading_day=reading_day, local=local):
                raise ValidationError("%s ya tiene registro en este mes" % local)
        except ObjectDoesNotExist:
            pass


class RegisterUpdateForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['plan', 'reading']
        widgets = {
            'plan': forms.NumberInput(attrs={'class': 'form-control'}),
            'reading': forms.NumberInput(attrs={'class': 'form-control'}),
        }
