# Generated by Django 4.1.6 on 2024-02-14 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cte', '0010_hoursrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoursrequest',
            name='reviewed',
            field=models.BooleanField(default=False),
        ),
    ]