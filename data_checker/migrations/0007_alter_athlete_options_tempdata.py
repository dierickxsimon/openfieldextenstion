# Generated by Django 4.2.4 on 2023-08-18 16:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('data_checker', '0006_athlete_avg_jogging2_athlete_max_jogging2'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='athlete',
            options={'ordering': ['-max_td']},
        ),
        migrations.CreateModel(
            name='TempData',
            fields=[
                ('temp_td', models.IntegerField(blank=True, default=0, null=True)),
                ('temp_sprinting', models.IntegerField(blank=True, default=0, null=True)),
                ('temp_HSR', models.IntegerField(blank=True, default=0, null=True)),
                ('temp_running', models.IntegerField(blank=True, default=0, null=True)),
                ('temp_jogging', models.IntegerField(blank=True, default=0, null=True)),
                ('temp_jogging2', models.IntegerField(blank=True, default=0, null=True)),
                ('temp_walking', models.IntegerField(blank=True, default=0, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('athlete', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data_checker.athlete')),
            ],
        ),
    ]
