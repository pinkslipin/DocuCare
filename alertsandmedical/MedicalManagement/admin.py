from django.contrib import admin
from .models import Prescription, Patient, Appointment

admin.site.register(Prescription)
admin.site.register(Patient)
admin.site.register(Appointment)