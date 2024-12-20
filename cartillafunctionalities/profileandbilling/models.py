from django.db import models
from django.contrib.auth.models import User

class BillingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_description = models.CharField(max_length=255)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # New field
    status = models.CharField(max_length=20, default='Unpaid')  # New field: 'Unpaid', 'Partially Paid', 'Paid'
    date_issued = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    @property
    def balance_due(self):
        return self.amount_due - self.paid_amount  # Calculate remaining balance

    def update_status(self):
        if self.paid_amount == 0:
            self.status = 'Unpaid'
        elif self.paid_amount < self.amount_due:
            self.status = 'Partially Paid'
        else:
            self.status = 'Paid'
        self.save()

    def __str__(self):
        return f"BillingRecord for {self.user.username} - {self.service_description} ({self.status})"

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Credit Card', 'Credit Card'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cash', 'Cash'),
        ('Gcash','Gcash'),
    ]
    billing_record = models.ForeignKey(BillingRecord, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"Payment of {self.payment_amount} for {self.billing_record.service_description}"

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return self.full_name