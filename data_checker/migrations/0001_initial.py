# Generated by Django 4.2.4 on 2023-08-14 19:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activities',
            fields=[
                ('name', models.CharField(max_length=300)),
                ('date', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('name', models.CharField(max_length=300)),
                ('max_td', models.IntegerField(blank=True, null=True)),
                ('max_sprinting', models.IntegerField(blank=True, null=True)),
                ('max_HSR', models.IntegerField(blank=True, null=True)),
                ('max_running', models.IntegerField(blank=True, null=True)),
                ('max_jogging', models.IntegerField(blank=True, null=True)),
                ('max_walking', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('td', models.IntegerField(blank=True, null=True)),
                ('sprinting', models.IntegerField(blank=True, null=True)),
                ('HSR', models.IntegerField(blank=True, null=True)),
                ('running', models.IntegerField(blank=True, null=True)),
                ('jogging', models.IntegerField(blank=True, null=True)),
                ('walking', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data_checker.activities')),
                ('athlete', models.ManyToManyField(blank=True, null=True, to='data_checker.athlete')),
            ],
        ),
    ]
