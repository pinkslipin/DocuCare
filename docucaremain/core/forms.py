from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.forms import TextInput, DateInput
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

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254)

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
                self.user_cache = authenticate(username=user.username, password=password)
                if self.user_cache is None:
                    raise ValidationError('Invalid email or password')
            except User.DoesNotExist:
                raise ValidationError('Invalid email or password')
        return self.cleaned_data

# Patient Registration Form
class PatientRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(max_length=255, required=True)
    contact_number = forms.CharField(max_length=15, required=True)
    medical_history = forms.CharField(max_length=1000, required=False)
    email = forms.EmailField(required=True)  # New email field
    blood_type = forms.CharField(max_length=3, required=False)
    height = forms.CharField(max_length=10, required=False)
    weight = forms.CharField(max_length=10, required=False)
    allergies = forms.CharField(max_length=255, required=False)
    sex = forms.CharField(max_length=10, required=False)
    age = forms.IntegerField(required=False)
    occupation = forms.CharField(max_length=100, required=False)
    marital_status = forms.CharField(max_length=50, required=False)
    emergency_contact = forms.CharField(max_length=255, required=False)

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
                email=self.cleaned_data['email'],  # Save email in PatientProfile
                blood_type=self.cleaned_data.get('blood_type', ''),
                height=self.cleaned_data.get('height', ''),
                weight=self.cleaned_data.get('weight', ''),
                allergies=self.cleaned_data.get('allergies', ''),
                sex=self.cleaned_data.get('sex', ''),
                age=self.cleaned_data.get('age', None),
                occupation=self.cleaned_data.get('occupation', ''),
                marital_status=self.cleaned_data.get('marital_status', ''),
                emergency_contact=self.cleaned_data.get('emergency_contact', '')
            )
        return user


# Patient Profile Form
class PatientProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = PatientProfile
        fields = [
            'full_name', 'date_of_birth', 'address', 'contact_number', 'medical_history',
            'blood_type', 'height', 'weight', 'allergies', 'sex', 'age', 'occupation',
            'marital_status', 'emergency_contact'
        ]


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
#if mag ka error ang code idelete ni nga function
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password != password_confirmation:
            self.add_error('password_confirmation', "Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = User.objects.get(username=self.cleaned_data['username'])
        user.email = self.cleaned_data['email']

        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return super().save(commit)

class AddNotesForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

# Consultation Form (Shared)
from django.forms import HiddenInput, DateInput, TextInput

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['doctor', 'date', 'time', 'description']
        widgets = {
            'doctor': HiddenInput(),  # Hidden field for doctor
            'time': TextInput(attrs={'readonly': 'readonly'}),  # Non-editable time field
            'date': DateInput(attrs={'type': 'date'}),          # HTML5 datepicker
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.all()
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
