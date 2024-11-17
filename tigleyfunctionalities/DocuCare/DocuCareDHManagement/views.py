from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Consultation, Doctor, MedicalTest
from .forms import ConsultationForm, DoctorForm, EditProfileForm, MedicalTestForm, RegisterForm
from django.contrib.auth.models import User

@login_required
def homepage(request):
    return render(request, 'homepage.html')

def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        doctor_form = DoctorForm(request.POST)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save(commit=False)
            user.is_staff = True  # Mark the user as staff to differentiate from patients
            user.save()
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            login(request, user)
            return redirect('homepage')
    else:
        user_form = RegisterForm()
        doctor_form = DoctorForm()
    return render(request, 'register.html', {'user_form': user_form, 'doctor_form': doctor_form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def doctor_list(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            user.is_staff = True  # Make the user a staff member
            user.save()
            doctor = form.save(commit=False)
            doctor.user = user
            doctor.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    
    doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'form': form, 'doctors': doctors})

@login_required
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctor_list.html', {'form': form, 'doctors': Doctor.objects.all()})

@login_required
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        user = doctor.user
        doctor.delete()
        user.delete() 
        return redirect('doctor_list')
    return render(request, 'doctor_confirm_delete.html', {'doctor': doctor})

@login_required
def edit_profile(request):
    user = request.user
    doctor = user.doctor  

    if request.method == 'POST':
        form = EditProfileForm(request.POST, user=user, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('profile_view')  
    else:
        form = EditProfileForm(instance=doctor, user=user)

    return render(request, 'edit_profile.html', {'form': form})

@login_required
def medical_test_management(request):
    tests = MedicalTest.objects.all()
    form = MedicalTestForm()
    if request.method == "POST":
        form = MedicalTestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medical_test_management')
    return render(request, 'medical_test_management.html', {'form': form, 'tests': tests})

@login_required
def medical_test_create(request):
    if request.method == 'POST':
        form = MedicalTestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medical_test_management')
    else:
        form = MedicalTestForm()
    return render(request, 'medical_test_form.html', {'form': form})

@login_required
def medical_test_update(request, test_id):
    test = get_object_or_404(MedicalTest, id=test_id)
    form = MedicalTestForm(request.POST or None, instance=test)
    if form.is_valid():
        form.save()
        return redirect('medical_test_management')
    return render(request, 'medical_test_form.html', {'form': form})

@login_required
def medical_test_delete(request, test_id):
    test = get_object_or_404(MedicalTest, id=test_id)
    if request.method == "POST":
        test.delete()
        return redirect('medical_test_management')
    return render(request, 'medical_test_confirm_delete.html', {'test': test})

@login_required
def book_consultation(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'consultation_success.html')
    else:
        form = ConsultationForm()
    return render(request, 'book_consultation.html', {'form': form})

@login_required
def consultation_list(request):
    consultations = Consultation.objects.all()
    return render(request, 'consultation_list.html', {'consultations': consultations})
