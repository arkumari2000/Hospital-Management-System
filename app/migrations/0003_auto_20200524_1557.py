# Generated by Django 3.0.5 on 2020-05-24 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_appointment_doctor_patient_person_receptionist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.PositiveSmallIntegerField(
                choices=[(1, 'doctor'), (2, 'patient'), (3, 'HR'), (4, 'Receptionist')],
                null=True,
            ),
        ),
    ]
