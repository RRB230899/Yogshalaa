# Generated by Django 4.1.9 on 2023-05-23 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing_page', '0003_profile_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='uid',
            field=models.CharField(default='<function uuid5 at 0x00000139F0D1D360>', max_length=200, unique=True),
        ),
    ]
