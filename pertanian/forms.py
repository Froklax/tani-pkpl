from django import forms
from django.utils.html import strip_tags
from .models import Plant, Field, Planting

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'plant_type', 'harvest_time', 'description', 'seed_price']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
                'placeholder': 'Plant name'
            }),
            'plant_type': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
                'placeholder': 'Plant type'
            }),
            'harvest_time': forms.NumberInput(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
                'placeholder': 'Harvest time in days'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
                'rows': 3,
                'placeholder': 'Plant description'
            }),
            'seed_price': forms.NumberInput(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
                'placeholder': 'Seed price per unit'
            }),
        }

    def clean_name(self):
        return strip_tags(self.cleaned_data.get('name'))

    def clean_description(self):
        return strip_tags(self.cleaned_data.get('description'))

class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['field_name', 'area', 'address', 'is_active']

        widgets = {
            'field_name': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
                'placeholder': 'Field name'
            }),
            'area': forms.NumberInput(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
                'placeholder': 'Field area in hectares'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
                'rows': 3,
                'placeholder': 'Full address of the field'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'ml-2'
            }),
        }

    def clean_field_name(self):
        return strip_tags(self.cleaned_data.get('field_name'))

    def clean_address(self):
        return strip_tags(self.cleaned_data.get('address'))

class PlantingForm(forms.ModelForm):
    class Meta:
        model = Planting
        fields = ['field', 'plant', 'planting_date', 'seed_count', 'note']

        widgets = {
            'field': forms.Select(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
            }),
            'plant': forms.Select(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
            }),
            'planting_date': forms.DateInput(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
                'type': 'date'
            }),
            'seed_count': forms.NumberInput(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
                'placeholder': 'Number of seeds planted'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
            }),
        }

    def clean_note(self):
        return strip_tags(self.cleaned_data.get('note'))