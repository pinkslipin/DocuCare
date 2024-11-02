from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import PatientProfileForm, PatientRegistrationForm, BillingRecordForm, PaymentForm

from datetime import date
from .models import BillingRecord, PatientProfile, Payment
from .forms import BillingRecordForm, PaymentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
import logging


# Home page view

@login_required
def home(request):
    # Check if the user is a staff member
    can_create_billing = request.user.is_staff
    return render(request, 'home.html', {'can_create_billing': can_create_billing})

# Registration view
def register(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # This will save the user and set the password
        
            # Create a PatientProfile for the new user
            PatientProfile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                address=form.cleaned_data['address'],
                contact_number=form.cleaned_data['contact_number'],
                medical_history=form.cleaned_data['medical_history']
            )

            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = PatientRegistrationForm()
    return render(request, 'register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            if user.is_staff:
                return redirect('billing_records')  # Redirect staff to billing records
            else:
                return redirect('user_home')  # Redirect patients
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
    return render(request, 'login.html')

logger = logging.getLogger(__name__)
# View to list all billing records for a user
@login_required
def billing_records(request):
    records = BillingRecord.objects.filter(user=request.user).exclude(status='Paid')
    
    # Update the status based on amounts
    for record in records:
        if record.paid_amount > 0 and record.balance_due > 0:
            record.status = 'Partially Paid'
        elif record.balance_due == 0:
            record.status = 'Paid'
        else:
            record.status = 'Unpaid'
    
    today = date.today() 
    logger.info(f"User: {request.user}, Billing Records: {records}")
    return render(request, 'billing_records.html', {'records': records, 'today': today})

# Only allow staff users to create billing records
@user_passes_test(lambda u: u.is_staff)
def create_billing_record(request):
    if request.method == 'POST':
        form = BillingRecordForm(request.POST)
        if form.is_valid():
            billing_record = form.save(commit=False)
            billing_record.save()  # Save the billing record
            messages.success(request, 'Billing record created successfully.')
            return redirect('billing_records')
    else:
        form = BillingRecordForm()
    return render(request, 'create_billing_record.html', {'form': form})


# View to process a payment
# Make this view accessible to both patients and staff
@login_required
def process_payment(request, record_id):
    billing_record = get_object_or_404(BillingRecord, id=record_id)
    # Ensure only the owner (patient) or staff can access
    if request.user != billing_record.user and not request.user.is_staff:
        return redirect('home')  # Redirect unauthorized users

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.billing_record = billing_record
            billing_record.paid_amount += payment.payment_amount
            billing_record.update_status()
            payment.save()
            messages.success(request, 'Payment processed successfully.')
            return redirect('patient_billing_records')  # Redirect back to patient billing records
        else:
            messages.error(request, 'There was an issue with your payment.')
    else:
        form = PaymentForm()
    return render(request, 'process_payment.html', {'form': form, 'billing_record': billing_record})



##patient stuff

@login_required
def list_patients(request):
    patients = User.objects.all()  # Assuming patients are User instances
    return render(request, 'list_patients.html', {'patients': patients})

@login_required
def view_patient(request, patient_id):
    # Get the PatientProfile associated with the User
    patient_profile = get_object_or_404(PatientProfile, user__id=patient_id)
    return render(request, 'view_patient.html', {'patient': patient_profile})

@login_required
def update_patient(request, patient_id):
    patient_profile = get_object_or_404(PatientProfile, user__id=patient_id)
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient profile updated successfully.')
            return redirect('list_patients')
        else:
            messages.error(request, 'There were errors in your form. Please correct them.')

    else:
        form = PatientProfileForm(instance=patient_profile)

    return render(request, 'update_patient.html', {'form': form, 'patient': patient_profile})

@login_required
def delete_patient(request, patient_id):
    patient = get_object_or_404(User, id=patient_id)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient profile deleted successfully.')
        return redirect('list_patients')
    return render(request, 'delete_patient.html', {'patient': patient})

@login_required
def patient_billing_records(request):
    records = BillingRecord.objects.filter(user=request.user).exclude(status='Paid')
    
    # Update the status based on amounts
    for record in records:
        if record.paid_amount > 0 and record.balance_due > 0:
            record.status = 'Partially Paid'
        elif record.balance_due == 0:
            record.status = 'Paid'
        else:
            record.status = 'Unpaid'
    
    return render(request, 'patient_billing_records.html', {'records': records})

@login_required
def user_home(request):
    return render(request, 'user_home.html')

@login_required
def logout_view(request):
    logout(request)  # This logs out the user
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')  # Redirect to the login page or home page