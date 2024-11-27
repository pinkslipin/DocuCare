from datetime import date
from django.db import models
from django.contrib.auth.models import User

# Doctor model (Admin-Specific)
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)  # Provide a default value
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
    medical_history = models.CharField(max_length=1000)
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)  # New email field

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
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('complete', 'Complete'),
    ]

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='consultations')
    date = models.DateField()
    description = models.TextField()
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        if self.notes:
            self.status = 'complete'
        else:
            self.status = 'pending'
        super().save(*args, **kwargs)

    def can_add_notes(self):
        return self.date == date.today()

    def __str__(self):
        return f"Consultation with {self.doctor} on {self.date}"


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


# MedicalTestApplication model
class MedicalTestApplication(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    medical_test = models.ForeignKey(MedicalTest, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default='Unpaid')  # 'Unpaid', 'Partially Paid', 'Paid'
    payment_completion_date = models.DateTimeField(null=True, blank=True)

    def update_payment_status(self):
        billing_record = BillingRecord.objects.filter(
            patient=self.patient,
            service_description=f"Medical Test: {self.medical_test.name}"
        ).first()
        if billing_record:
            self.payment_status = billing_record.status
            if billing_record.status == 'Paid':
                self.payment_completion_date = billing_record.payment_set.latest('payment_date').payment_date
            self.save()

    def __str__(self):
        return f"{self.patient.full_name} applied for {self.medical_test.name}"


# Patient model
class Patient(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


# Prescription model
class Prescription(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    medication = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prescription for {self.patient.full_name} - {self.medication}"


# Appointment model
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, default='scheduled')
    
    def __str__(self):
        return f"Appointment for {self.patient.name} on {self.date}"
