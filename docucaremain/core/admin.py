from django.contrib import admin
from .models import BillingRecord, Doctor, HealthProvider, MedicalTest, PatientProfile, Consultation, Recommendation,  Prescription,  MedicalTestApplication

admin.site.register(Doctor)
admin.site.register(HealthProvider)
admin.site.register(PatientProfile)
admin.site.register(Consultation)
admin.site.register(Recommendation)
admin.site.register(BillingRecord)
admin.site.register(MedicalTest)
admin.site.register(Prescription)
admin.site.register(MedicalTestApplication)