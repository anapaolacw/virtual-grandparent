# Generated by Django 4.0.2 on 2022-08-17 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_helper_isverified'),
    ]

    operations = [
        migrations.AddField(
            model_name='helpcandidates',
            name='description',
            field=models.TextField(default='I would like to offer my help since I have practice on that', max_length=1000),
            preserve_default=False,
        ),
    ]
