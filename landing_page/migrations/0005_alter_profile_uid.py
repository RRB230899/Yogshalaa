# Generated by Django 4.1.9 on 2023-05-24 07:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('landing_page', '0004_alter_profile_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='uid',
            field=models.CharField(blank=True, default=uuid.uuid4, max_length=200, null=True, unique=True),
        ),
    ]
