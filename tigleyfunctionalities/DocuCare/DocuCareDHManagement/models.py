from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    contact_info = models.TextField()

    def __str__(self):
        return self.name

class HealthProvider(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField()

    def __str__(self):
        return self.name

class Patient(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField()
    assigned_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    notes = models.TextField()

    def __str__(self):
        return f"Consultation on {self.date} with {self.doctor}"

class Recommendation(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    recommendation_text = models.TextField()

    def __str__(self):
        return f"Recommendation for {self.consultation}"
    
class MedicalTest(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.name