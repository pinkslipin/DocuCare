from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import PatientRegistrationForm

from .models import BillingRecord, Payment
from .forms import BillingRecordForm, PaymentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


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
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
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
            return render(request, 'login_success.html')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
    return render(request, 'login.html')

# View to list all billing records for a user
@login_required
def billing_records(request):
    records = BillingRecord.objects.filter(user=request.user)
    return render(request, 'billing_records.html', {'records': records})

# Only allow staff users to create billing records
@user_passes_test(lambda u: u.is_staff)
def create_billing_record(request):
    if request.method == 'POST':
        form = BillingRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Billing record created successfully.')
            return redirect('billing_records')
    else:
        form = BillingRecordForm()
    return render(request, 'create_billing_record.html', {'form': form})

# View to process a payment
@login_required
def process_payment(request, record_id):
    billing_record = BillingRecord.objects.get(id=record_id, user=request.user)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.billing_record = billing_record
            payment.save()
            messages.success(request, 'Payment processed successfully.')
            return redirect('billing_records')
    else:
        form = PaymentForm()
    return render(request, 'process_payment.html', {'form': form, 'billing_record': billing_record})