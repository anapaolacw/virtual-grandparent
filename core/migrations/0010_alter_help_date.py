# Generated by Django 4.0.2 on 2022-08-15 09:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_help_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='help',
            name='date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
