# Generated by Django 4.1.6 on 2024-01-19 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cte', '0002_school_student_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='grad_year',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='student',
            name='major',
            field=models.CharField(max_length=80),
        ),
    ]