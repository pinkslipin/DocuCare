from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import (
    Doctor,
    PatientProfile,
    BillingRecord,
    Payment,
    MedicalTest,
    Consultation,
    Prescription,
    MedicalTestApplication
)

# Patient Registration Form
class PatientRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(max_length=255, required=True)
    contact_number = forms.CharField(max_length=15, required=True)
    medical_history = forms.CharField(max_length=1000, required=False)
    email = forms.EmailField(required=True)  # New email field

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create PatientProfile linked to the User
            PatientProfile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                address=self.cleaned_data['address'],
                contact_number=self.cleaned_data['contact_number'],
                medical_history=self.cleaned_data.get('medical_history', ''),
                email=self.cleaned_data['email']  # Save email in PatientProfile
            )
        return user


# Patient Profile Form
class PatientProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = PatientProfile
        fields = ['full_name', 'date_of_birth', 'address', 'contact_number', 'medical_history']


# Billing Record Form (Admin-Only)
class BillingRecordForm(forms.ModelForm):
    class Meta:
        model = BillingRecord
        fields = ['patient', 'service_description', 'amount_due', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = PatientProfile.objects.all()


# Payment Form (For Users)
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['billing_record', 'payment_amount', 'payment_method']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['billing_record'].queryset = BillingRecord.objects.exclude(status='Paid')


# Doctor Registration Form (Admin-Only)
class DoctorForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Doctor
        fields = ['email', 'name', 'specialization', 'contact_info']

    def save(self, commit=True):
        doctor = super().save(commit=False)
        doctor.email = self.cleaned_data['email']
        if commit:
            doctor.save()
        return doctor

# Medical Test Form (Admin-Only)
class MedicalTestForm(forms.ModelForm):
    class Meta:
        model = MedicalTest
        fields = ['name', 'description', 'price', 'availability']


# Medical Test Application Form
class MedicalTestApplicationForm(forms.ModelForm):
    class Meta:
        model = MedicalTestApplication
        fields = ['medical_test']


# Edit Profile Form (Admin-Only)
class EditProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(),
        required=False
    )
    password_confirmation = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(),
        required=False
    )

    class Meta:
        model = Doctor
        fields = ['name', 'specialization', 'contact_info']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        user = User.objects.get(username=self.cleaned_data['username'])
        user.email = self.cleaned_data['email']

        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return super().save(commit)


# Consultation Form (Shared)
class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['doctor', 'date', 'description']  # Exclude the patient field
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

# Prescription Form
class PrescriptionForm(forms.ModelForm):
    patient = forms.ModelChoiceField(queryset=PatientProfile.objects.all(), label="Patient")
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Prescription
        fields = ['patient', 'date', 'time', 'medication']
        widgets = {
            'medication': forms.TextInput(attrs={'placeholder': 'Enter Medication'}),
        }
