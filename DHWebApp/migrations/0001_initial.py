# Generated by Django 3.0 on 2020-04-18 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('hregno', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('hname', models.CharField(max_length=100)),
                ('fname', models.CharField(max_length=50)),
                ('lname', models.CharField(max_length=50)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='M', max_length=10)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=12)),
                ('adharid', models.CharField(max_length=12)),
                ('password', models.CharField(max_length=50)),
                ('contry', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('zipcode', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Hstaff',
            fields=[
                ('designation', models.CharField(choices=[('AD', 'Admin'), ('AC', 'Accountat'), ('DC', 'Doctor'), ('CS', 'Clerical Staff'), ('RC', 'Receptionist'), ('JS', 'Janitorial Staff'), ('LT', 'Lab Technician'), ('NR', 'Nurse'), ('PS', 'Phycisian'), ('HK', 'House Keeping')], default='DC', max_length=150)),
                ('fname', models.CharField(max_length=50)),
                ('lname', models.CharField(max_length=50)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='M', max_length=10)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=12)),
                ('adharid', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=50)),
                ('contry', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('zipcode', models.CharField(max_length=10)),
                ('hregno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DHWebApp.Hospital')),
            ],
        ),
    ]
