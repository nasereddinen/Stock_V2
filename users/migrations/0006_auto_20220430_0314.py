# Generated by Django 3.2.13 on 2022-04-30 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_reparation_materiel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reparation_materiel',
            name='place',
        ),
        migrations.AlterField(
            model_name='reparation_materiel',
            name='etat',
            field=models.CharField(blank=True, choices=[('1', 'en maintenance'), ('2', 'resolu'), ('3', 'en panne')], max_length=50, null=True),
        ),
    ]