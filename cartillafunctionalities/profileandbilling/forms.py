from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PatientProfile

from .models import BillingRecord, PatientProfile, Payment

class PatientRegistrationForm(UserCreationForm):  # Inherit from UserCreationForm
    full_name = forms.CharField(max_length=100, required=True)
    date_of_birth = forms.DateField(required=True)
    address = forms.CharField(max_length=255, required=True)
    contact_number = forms.CharField(max_length=15, required=True)
    medical_history = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'password1', 'password2']  # Add password fields

class BillingRecordForm(forms.ModelForm):
    class Meta:
        model = BillingRecord
        fields = ['user', 'service_description', 'amount_due', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.exclude(is_staff=True)  # Exclude staff users if needed

class PatientProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Use a date input widget

    class Meta:
        model = PatientProfile
        fields = ['full_name', 'date_of_birth', 'address', 'contact_number', 'medical_history']

        
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['billing_record', 'payment_amount', 'payment_method']

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        # Filter out "Paid" billing records
        self.fields['billing_record'].queryset = BillingRecord.objects.exclude(status='Paid')