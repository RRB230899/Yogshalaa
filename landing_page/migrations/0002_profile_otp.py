# Generated by Django 4.1.9 on 2023-05-20 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing_page', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='otp',
            field=models.CharField(default='******', max_length=6),
        ),
    ]
