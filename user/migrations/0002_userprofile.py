# Generated by Django 3.0.7 on 2020-07-04 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField(null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('premium', models.BooleanField(default=False)),
            ],
        ),
    ]
