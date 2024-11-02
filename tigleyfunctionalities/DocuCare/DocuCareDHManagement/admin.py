from django.contrib import admin
from .models import Doctor, HealthProvider, Patient, Consultation, Recommendation

admin.site.register(Doctor)
admin.site.register(HealthProvider)
admin.site.register(Patient)
admin.site.register(Consultation)
admin.site.register(Recommendation)