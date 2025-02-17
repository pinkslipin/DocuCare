# Generated by Django 5.1.2 on 2024-11-01 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileandbilling', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingrecord',
            name='paid_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='billingrecord',
            name='status',
            field=models.CharField(default='Unpaid', max_length=20),
        ),
    ]
