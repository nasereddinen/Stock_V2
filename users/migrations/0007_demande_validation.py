# Generated by Django 3.2.13 on 2022-05-01 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20220430_0314'),
    ]

    operations = [
        migrations.AddField(
            model_name='demande',
            name='validation',
            field=models.CharField(blank=True, choices=[('1', 'livrer'), ('2', 'en cours')], max_length=50, null=True),
        ),
    ]
