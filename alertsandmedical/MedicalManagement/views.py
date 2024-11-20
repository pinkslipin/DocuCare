# views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import Prescription, Patient
from .forms import PrescriptionForm

class PrescriptionListView(ListView):
    model = Prescription
    template_name = 'medical/prescription_list.html'
    context_object_name = 'prescriptions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Prescriptions'
        return context

class PrescriptionCreateView(CreateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'medical/prescription_form.html'
    success_url = reverse_lazy('medical:prescription_list')  # Redirect to the list after adding

    def form_valid(self, form):
        # Get the patient name from the form input
        patient_name = form.cleaned_data['patient_name']
        
        # Fetch or create a Patient instance by name
        patient, created = Patient.objects.get_or_create(name=patient_name)
        
        # Assign the patient instance to the prescription before saving
        form.instance.patient = patient
        return super().form_valid(form)