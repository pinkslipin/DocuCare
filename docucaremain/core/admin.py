from django.contrib import admin
from .models import Doctor, HealthProvider, MedicalTest, PatientProfile, Consultation, Recommendation

admin.site.register(Doctor)
admin.site.register(HealthProvider)
admin.site.register(PatientProfile)
admin.site.register(Consultation)
admin.site.register(Recommendation)
admin.site.register(MedicalTest)