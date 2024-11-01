from django import forms
from django.contrib.auth.models import User

from .models import BillingRecord, Payment

class PatientRegistrationForm(forms.ModelForm):
    full_name = forms.CharField(max_length=100, required=True)
    date_of_birth = forms.DateField(required=True)
    address = forms.CharField(max_length=255, required=True)
    contact_number = forms.CharField(max_length=15, required=True)
    medical_history = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'full_name', 'date_of_birth', 'address', 'contact_number', 'medical_history']

class BillingRecordForm(forms.ModelForm):
    class Meta:
        model = BillingRecord
        fields = ['user', 'service_description', 'amount_due', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['billing_record', 'payment_amount', 'payment_method']
