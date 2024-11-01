from django.db import models
from django.contrib.auth.models import User

class BillingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_description = models.CharField(max_length=255)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    date_issued = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    def __str__(self):
        return f"BillingRecord for {self.user.username} - {self.service_description}"

class Payment(models.Model):
    billing_record = models.ForeignKey(BillingRecord, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment of {self.payment_amount} for {self.billing_record.service_description}"
