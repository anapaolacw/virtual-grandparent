# Generated by Django 4.0.2 on 2022-08-15 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_help_datetime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='help',
            old_name='dateTime',
            new_name='date',
        ),
    ]