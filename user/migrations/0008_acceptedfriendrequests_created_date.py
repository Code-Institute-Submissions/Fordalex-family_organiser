# Generated by Django 3.0.7 on 2020-07-16 22:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_acceptedfriendrequests'),
    ]

    operations = [
        migrations.AddField(
            model_name='acceptedfriendrequests',
            name='created_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
