# Generated by Django 4.1.5 on 2023-04-01 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lab_App', '0002_attendance_barcode_attendance_new_barcode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance_new',
            name='Barcode',
            field=models.CharField(default=None, max_length=5),
        ),
    ]
