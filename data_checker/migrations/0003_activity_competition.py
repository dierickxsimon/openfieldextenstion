# Generated by Django 4.2.4 on 2023-08-15 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_checker', '0002_activity_data_alter_activity_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='competition',
            field=models.BooleanField(default=False),
        ),
    ]
