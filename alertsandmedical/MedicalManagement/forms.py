# forms.py
from django import forms
from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    patient_name = forms.CharField(label="Patient", max_length=100)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Prescription
        fields = ['appt_id', 'patient_name', 'date', 'time', 'medication']
        widgets = {
            'appt_id': forms.TextInput(attrs={'placeholder': 'Enter Appointment ID'}),
            'medication': forms.TextInput(attrs={'placeholder': 'Enter Medication'}),
        }