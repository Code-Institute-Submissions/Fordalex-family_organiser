# Generated by Django 3.0.7 on 2020-07-16 22:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('message', '0004_messagenotification'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagenotification',
            name='sent_from',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_noti_sent_from', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='messagenotification',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_noti_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
