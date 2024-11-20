from django.db import models
from django.contrib.auth.models import User

# Doctor model (Admin-Specific)
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# PatientProfile model (Shared between Admin and User)
class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return self.full_name


# HealthProvider model (Admin-Specific)
class HealthProvider(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField()

    def __str__(self):
        return self.name


# BillingRecord model (User-Specific)
class BillingRecord(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)  # Reference PatientProfile
    service_description = models.CharField(max_length=255)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=20, default='Unpaid')  # 'Unpaid', 'Partially Paid', 'Paid'
    date_issued = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    @property
    def balance_due(self):
        return self.amount_due - self.paid_amount

    def update_status(self):
        if self.paid_amount == 0:
            self.status = 'Unpaid'
        elif self.paid_amount < self.amount_due:
            self.status = 'Partially Paid'
        else:
            self.status = 'Paid'
        self.save()

    def __str__(self):
        return f"BillingRecord for {self.patient.full_name} - {self.service_description} ({self.status})"


# Payment model (User-Specific)
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Credit Card', 'Credit Card'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cash', 'Cash'),
        ('Gcash', 'Gcash'),
    ]
    billing_record = models.ForeignKey(BillingRecord, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"Payment of {self.payment_amount} for {self.billing_record.service_description}"


# Consultation model (Shared between Admin and User)
class Consultation(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    notes = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return f"Consultation on {self.date} with {self.doctor}"


# Recommendation model (Admin-Specific)
class Recommendation(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    recommendation_text = models.TextField()

    def __str__(self):
        return f"Recommendation for {self.consultation}"


# MedicalTest model (Admin-Specific)
class MedicalTest(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.name
