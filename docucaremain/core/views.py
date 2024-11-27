from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView

from .forms import (
    AddNotesForm,
    PatientProfileForm,
    PatientRegistrationForm,
    BillingRecordForm,
    PaymentForm,
    DoctorForm,
    EditProfileForm,
    MedicalTestForm,
    ConsultationForm,
    PrescriptionForm,
    MedicalTestApplicationForm,
    EmailAuthenticationForm,
)
from .models import (
    BillingRecord,
    PatientProfile,
    Payment,
    Doctor,
    MedicalTest,
    Consultation,
    Prescription,
    Patient,
    MedicalTestApplication
)
from datetime import timedelta

def landing_page(request):
    return render(request, 'landing_page.html')


# Unified Home Page
def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_home')
        return redirect('user_home')
    return redirect('landing_page')


# Admin Home Page
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_home(request):
    doctors = Doctor.objects.all()
    patients = PatientProfile.objects.all()
    billing_records = BillingRecord.objects.all()
    consultations = Consultation.objects.all()
    medical_tests = MedicalTest.objects.all()

    context = {
        'doctors': doctors,
        'patients': patients,
        'billing_records': billing_records,
        'consultations': consultations,
        'medical_tests': medical_tests,
    }
    return render(request, 'admin/admin_home.html', context)

# User Home Page
@login_required
def user_home(request):
    user = request.user
    patient_profile = get_object_or_404(PatientProfile, user=user)
    billing_records = BillingRecord.objects.filter(patient=patient_profile)
    prescriptions = Prescription.objects.filter(patient=patient_profile)
    medical_tests = MedicalTestApplication.objects.filter(patient=patient_profile)

    context = {
        'patient_profile': patient_profile,
        'billing_records': billing_records,
        'prescriptions': prescriptions,
        'medical_tests': medical_tests,
    }
    return render(request, 'user/user_home.html', context)

# Patient Registration View
def register_patient(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient account created successfully!')
            return redirect('login')
    else:
        user_form = UserCreationForm()
        form = PatientRegistrationForm()
    return render(request, 'register_patient.html', {'form': form})

# Doctor Registration View
@login_required
@user_passes_test(lambda u: u.is_superuser)
def register_doctor(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        doctor_form = DoctorForm(request.POST)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save(commit=False)
            user.is_staff = True
            user.email = doctor_form.cleaned_data['email']  # Save email in User model
            user.save()
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            messages.success(request, 'Doctor account created successfully!')
            return redirect('login')  # Redirect to login page
    else:
        user_form = UserCreationForm()
        doctor_form = DoctorForm()
    return render(request, 'register_doctor.html', {'user_form': user_form, 'doctor_form': doctor_form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if request.user.is_staff:
                return redirect('admin_home')
            else:
                return redirect('user_home')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

# List of Doctors (Admin-Only)
@login_required
@user_passes_test(lambda u: u.is_staff)
def doctor_list(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save(commit=False)
            user = User.objects.create_user(
                username=form.cleaned_data['name'],  # Assume name is unique
                email=form.cleaned_data['contact_info'],
                password='password',  # Add proper handling for passwords
                is_staff=True
            )
            doctor.user = user
            doctor.save()
            messages.success(request, 'Doctor added successfully.')
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    doctors = Doctor.objects.all()
    return render(request, 'admin/doctor_list.html', {'form': form, 'doctors': doctors})

@login_required
def view_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'admin/view_doctor.html', {'doctor': doctor})

@login_required
def medical_test_update(request, test_id):
    test = get_object_or_404(MedicalTest, id=test_id)
    form = MedicalTestForm(request.POST or None, instance=test)
    if form.is_valid():
        form.save()
        return redirect('medical_test_management')
    return render(request, 'admin/medical_test_form.html', {'form': form})

@login_required
def medical_test_delete(request, test_id):
    test = get_object_or_404(MedicalTest, id=test_id)
    if request.method == "POST":
        test.delete()
        return redirect('medical_test_management')
    return render(request, 'admin/medical_test_confirm_delete.html', {'test': test})

# Doctor Profile Edit (Admin-Only)
@login_required
def edit_profile(request):
    user = request.user  # This refers to the User instance
    doctor = get_object_or_404(Doctor, user=user)

    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, user=user, instance=doctor)
        doctor_form = DoctorForm(request.POST, instance=doctor)
        if user_form.is_valid() and doctor_form.is_valid():
            # Save user-related fields
            updated_user = user_form.save(commit=False)  # Save user-related fields without committing
            user.username = user_form.cleaned_data['username']
            user.email = user_form.cleaned_data['email']
            if user_form.cleaned_data['password']:
                user.set_password(user_form.cleaned_data['password'])  # Set password on the User object
                update_session_auth_hash(request, user)  # Maintain session after password change
            user.save()

            # Save doctor-related fields
            doctor_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('edit_profile')
    else:
        user_form = EditProfileForm(instance=doctor, user=user)
        doctor_form = DoctorForm(instance=doctor)

    return render(request, 'admin/edit_profile.html', {'user_form': user_form, 'doctor_form': doctor_form})
#tests comment
# Medical Test Management (Admin-Only)
@login_required
@user_passes_test(lambda u: u.is_staff)
def medical_test_management(request):
    tests = MedicalTest.objects.all()
    if request.method == 'POST':
        form = MedicalTestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medical test added successfully.')
            return redirect('medical_test_management')
    else:
        form = MedicalTestForm()
    return render(request, 'admin/medical_test_management.html', {'form': form, 'tests': tests})

# Create Medical Test (Admin-Only)
@login_required
@user_passes_test(lambda u: u.is_staff)
def medical_test_create(request):
    if request.method == 'POST':
        form = MedicalTestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medical test created successfully.')
            return redirect('medical_test_management')
    else:
        form = MedicalTestForm()
    return render(request, 'admin/medical_test_form.html', {'form': form})

@login_required
def view_own_profile(request):
    patient_profile = get_object_or_404(PatientProfile, user=request.user)
    return render(request, 'user/view_own_profile.html', {'patient': patient_profile})

@login_required
def patient_billing_records(request):
    records = BillingRecord.objects.filter(patient__user=request.user)
    
    # Update the status based on amounts
    for record in records:
        if record.paid_amount > 0 and record.balance_due > 0:
            record.status = 'Partially Paid'
        elif record.balance_due == 0:
            record.status = 'Completed'
        else:
            record.status = 'Unpaid'
    
    return render(request, 'user/patient_billing_records.html', {'records': records})

@login_required
def delete_billing_record(request, record_id):
    record = get_object_or_404(BillingRecord, id=record_id)
    if record.patient.user == request.user:
        if record.balance_due == 0.00:
            record.delete()
            messages.success(request, 'Billing record deleted successfully.')
        else:
            messages.error(request, 'You can only delete completed billing records.')
    else:
        messages.error(request, 'You do not have permission to delete this billing record.')
    return redirect('patient_billing_records')

# Create Billing Record (Admin-Only)
# Only allow staff users to create billing records
@user_passes_test(lambda u: u.is_staff)
def create_billing_record(request):
    if request.method == 'POST':
        form = BillingRecordForm(request.POST)
        if form.is_valid():
            billing_record = form.save(commit=False)
            billing_record.save()  # Save the billing record
            messages.success(request, f'Billing record created successfully for {billing_record.patient.user.username}.')
            return redirect('create_billing_record')  # Reload the same page
    else:
        form = BillingRecordForm()
    return render(request, 'admin/create_billing_record.html', {'form': form})

@login_required
def cancel_update_patient(request, patient_id):
    patient_profile = get_object_or_404(PatientProfile, user__id=patient_id)
    
    if request.user.is_staff:
        return redirect('list_patients')  # Redirect to patient list for staff
    else:
        return redirect('view_own_profile')  # Redirect to own profile for patients
    
# Patient List (Admin-Only)
@login_required
@user_passes_test(lambda u: u.is_staff)
def list_patients(request):
    patients = PatientProfile.objects.all()
    return render(request, 'admin/list_patients.html', {'patients': patients})

# Patient Profile (Admin or Self)
@login_required
def view_patient(request, patient_id):
    patient = get_object_or_404(PatientProfile, id=patient_id)
    return render(request, 'user/view_patient.html', {'patient': patient})

# Update Patient (Admin or Self)
@login_required
def update_patient(request, patient_id):
    patient = get_object_or_404(PatientProfile, id=patient_id)
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient profile updated successfully.')
            return redirect('view_patient', patient_id=patient.id)  # Redirect to view_patient
    else:
        form = PatientProfileForm(instance=patient)
    return render(request, 'user/update_patient.html', {'form': form, 'patient': patient})

# Delete Patient (Admin-Only)
@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_patient(request, patient_id):
    patient = get_object_or_404(PatientProfile, id=patient_id)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient deleted successfully.')
        return redirect('list_patients')
    return render(request, 'admin/delete_patient.html', {'patient': patient})

# Update Doctor Profile (Admin-Only)
@login_required
@user_passes_test(lambda u: u.is_staff)
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor updated successfully.')
            return redirect('doctor_list')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'admin/doctor_list.html', {'form': form}) #if ilisan nig doctor_form lain ang style mugawas  

# Delete Doctor (Admin-Only)
@login_required
@user_passes_test(lambda u: u.is_staff)
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        messages.success(request, 'Doctor deleted successfully.')
        return redirect('doctor_list')
    return render(request, 'admin/doctor_confirm_delete.html', {'doctor': doctor})

# Billing Records
@login_required
def billing_records(request):
    if request.user.is_staff:
        records = BillingRecord.objects.all()
    else:
        records = BillingRecord.objects.filter(patient__user=request.user)
    return render(request, 'billing_records.html', {'records': records})

# Process Payment
@login_required
def process_payment(request, record_id):
    record = get_object_or_404(BillingRecord, id=record_id)
    if not request.user.is_staff and request.user != record.patient.user:
        return redirect('home')
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.billing_record = record
            record.paid_amount += payment.payment_amount
            record.update_status()
            payment.save()
            messages.success(request, 'Payment was successful.')
            return redirect('patient_billing_records')
    else:
        form = PaymentForm()
    return render(request, 'user/process_payment.html', {'form': form, 'record': record})

# Book Consultation
@login_required
def book_consultation(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.patient = get_object_or_404(PatientProfile, user=request.user)
            consultation.save()
            messages.success(request, 'Consultation booked successfully.')
            return redirect('consultation_success')
    else:
        form = ConsultationForm()

    return render(request, 'admin/book_consultation.html', {'form': form})

@login_required
def consultation_success(request):
    return render(request, 'admin/consultation_success.html')

# List Consultations
@login_required
def consultation_list(request):
    if request.user.is_staff:
        consultations = Consultation.objects.all()
    else:
        consultations = Consultation.objects.filter(patient__user=request.user)
    return render(request, 'admin/consultation_list.html', {'consultations': consultations})

@login_required
def edit_own_profile(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('view_own_profile')
    else:
        form = PatientProfileForm(instance=patient)
    return render(request, 'user/update_patient.html', {'form': form, 'patient': patient})

class PrescriptionListView(ListView):
    model = Prescription
    template_name = 'admin/prescription_list.html'
    context_object_name = 'prescriptions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Prescriptions'
        return context

class PrescriptionCreateView(CreateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'admin/prescription_form.html'
    success_url = reverse_lazy('prescription_list')  # Redirect to the list after adding

    def form_valid(self, form):
        form.instance.patient = form.cleaned_data['patient']
        return super().form_valid(form)

class PrescriptionUpdateView(UpdateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'admin/prescription_form.html'
    success_url = reverse_lazy('prescription_list')

class PrescriptionDeleteView(DeleteView):
    model = Prescription
    template_name = 'admin/prescription_confirm_delete.html'
    success_url = reverse_lazy('prescription_list')

# Apply for Medical Test (User-Specific)
@login_required
def apply_medical_test(request):
    tests = MedicalTest.objects.all()
    if request.method == 'POST':
        form = MedicalTestApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.patient = request.user.patientprofile
            application.save()
            
            # Create a billing record for the medical test
            BillingRecord.objects.create(
                patient=application.patient,
                service_description=f"Medical Test: {application.medical_test.name}",
                amount_due=application.medical_test.price,
                due_date=application.application_date + timedelta(days=30)  # Example due date
            )
            
            messages.success(request, 'Applied for medical test successfully.')
            return redirect('user_home')
    else:
        form = MedicalTestApplicationForm()
    return render(request, 'user/apply_medical_test.html', {'form': form, 'tests': tests})


# View Medical Test Applications (Admin-Only)
@login_required
@user_passes_test(lambda u: u.is_staff)
def view_medical_test_applications(request):
    applications = MedicalTestApplication.objects.all()
    return render(request, 'admin/view_medical_test_applications.html', {'applications': applications})

@login_required
def view_prescriptions(request):
    prescriptions = Prescription.objects.filter(patient__user=request.user)
    return render(request, 'user/view_prescriptions.html', {'prescriptions': prescriptions})

@login_required
def add_notes(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    doctor = get_object_or_404(Doctor, user=request.user)
    
    if consultation.doctor != doctor:
        messages.error(request, 'You are not authorized to add notes to this consultation.')
        return redirect('consultation_list')
    
    if request.method == 'POST':
        form = AddNotesForm(request.POST, instance=consultation)
        if form.is_valid() and consultation.can_add_notes():
            form.save()
            messages.success(request, 'Notes added successfully. Consultation marked as complete.')
            return redirect('consultation_list')
    else:
        form = AddNotesForm(instance=consultation)

    return render(request, 'admin/add_notes.html', {'form': form, 'consultation': consultation})

@login_required
def view_consultations(request):
    consultations = Consultation.objects.filter(patient__user=request.user)
    return render(request, 'user/view_consultations.html', {'consultations': consultations})