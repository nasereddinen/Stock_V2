# Generated by Django 3.2.13 on 2022-06-10 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_alter_demande_devis_fournisseur'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demande_devis',
            name='fournisseur',
        ),
    ]
