# Generated by Django 5.2 on 2025-05-03 20:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='app.department'),
        ),
        migrations.AlterField(
            model_name='user',
            name='google_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
