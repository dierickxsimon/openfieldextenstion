# Generated by Django 4.2.4 on 2023-08-18 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_checker', '0005_alter_athlete_avg_hsr_alter_athlete_avg_jogging_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='athlete',
            name='avg_jogging2',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='athlete',
            name='max_jogging2',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
