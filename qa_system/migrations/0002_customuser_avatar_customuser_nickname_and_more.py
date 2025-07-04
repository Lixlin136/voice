# Generated by Django 5.0.3 on 2025-04-20 08:18

import qa_system.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("qa_system", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="avatar",
            field=models.ImageField(
                blank=True, null=True, upload_to=qa_system.models.user_avatar_path
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="nickname",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="phone",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="signature",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
