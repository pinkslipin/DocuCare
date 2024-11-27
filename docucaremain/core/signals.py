import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BillingRecord, MedicalTestApplication

logger = logging.getLogger(__name__)

@receiver(post_save, sender=BillingRecord)
def update_medical_test_application_payment_status(sender, instance, **kwargs):
    if instance.service_description.startswith("Medical Test:"):
        medical_test_name = instance.service_description.split(": ")[1]
        application = MedicalTestApplication.objects.filter(
            patient=instance.patient,
            medical_test__name=medical_test_name
        ).first()
        if application:
            application.update_payment_status()
            application.payment_completion_date = instance.date_issued
            application.save()
            logger.info(f"Updated payment status for medical test application {application.id} to {application.payment_status}")
        else:
            logger.warning(f"No medical test application found for patient {instance.patient.full_name} and test {medical_test_name}")