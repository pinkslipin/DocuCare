# Generated by Django 5.1.2 on 2024-11-01 13:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileandbilling', '0002_billingrecord_paid_amount_billingrecord_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('Credit Card', 'Credit Card'), ('Bank Transfer', 'Bank Transfer'), ('Cash', 'Cash'), ('Gcash', 'Gcash')], max_length=50),
        ),
        migrations.CreateModel(
            name='PatientProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('address', models.CharField(max_length=255)),
                ('contact_number', models.CharField(max_length=15)),
                ('medical_history', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]