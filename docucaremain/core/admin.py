from django.contrib import admin
from .models import Doctor, HealthProvider, MedicalTest, PatientProfile, Consultation, Recommendation, Patient, Prescription, Appointment

admin.site.register(Doctor)
admin.site.register(HealthProvider)
admin.site.register(PatientProfile)
admin.site.register(Consultation)
admin.site.register(Recommendation)
admin.site.register(MedicalTest)
admin.site.register(Patient)
admin.site.register(Prescription)
admin.site.register(Appointment)