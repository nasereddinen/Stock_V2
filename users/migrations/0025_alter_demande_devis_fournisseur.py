# Generated by Django 3.2.13 on 2022-06-10 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_alter_demande_devis_fournisseur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demande_devis',
            name='fournisseur',
            field=models.ManyToManyField(blank=True, to='users.Contact', verbose_name='Fournisseur'),
        ),
    ]