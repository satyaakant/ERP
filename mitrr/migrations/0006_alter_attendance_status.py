# Generated by Django 5.0.6 on 2024-09-03 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mitrr', '0005_attendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('P', 'Present'), ('A', 'Absent')], default='P', max_length=1),
        ),
    ]
