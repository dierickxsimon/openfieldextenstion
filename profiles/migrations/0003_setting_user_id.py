# Generated by Django 4.2.4 on 2023-08-17 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_setting'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='user_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.profile'),
        ),
    ]