# Generated by Django 4.1.6 on 2024-02-14 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cte', '0012_hoursrequest_program'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hoursrequest',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cte.job'),
        ),
    ]