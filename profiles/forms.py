from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from .models import Setting

class SettingForm(ModelForm):
    class Meta:
        model = Setting
        fields = ['athletes', 'start_date', 'end_date', 'parameter', 'competition_ratio']
        widgets = {
            'athletes': forms.CheckboxSelectMultiple(),
            'start_date' : forms.DateInput(attrs={'type': 'date'}),
            'end_date' : forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(SettingForm, self).__init__(*args, **kwargs)

        for name ,field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                self.add_error('end_date', "End date cannot be before start date.")