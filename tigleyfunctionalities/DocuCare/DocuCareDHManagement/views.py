from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Doctor
from .forms import DoctorForm, RegisterForm

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
            form.save()
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
        doctor.delete()
        return redirect('doctor_list')
    return render(request, 'doctor_confirm_delete.html', {'doctor': doctor})