# Generated by Django 3.0 on 2020-04-29 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DHWebApp', '0005_auto_20200427_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hstaff',
            name='profession',
            field=models.CharField(choices=[('AD', 'Admin'), ('AC', 'Accountant'), ('DC', 'Doctor'), ('CS', 'Clerical Staff'), ('RC', 'Receptionist'), ('JS', 'Janitorial Staff'), ('LT', 'Lab Technician'), ('NR', 'Nurse'), ('PS', 'Physcian'), ('HK', 'House Keeping')], default='AD', max_length=150),
        ),
    ]