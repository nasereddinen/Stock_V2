# Generated by Django 3.2.13 on 2022-05-02 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20220502_0506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reparation_materiel',
            name='observation',
            field=models.TextField(blank=True, null=True),
        ),
    ]
