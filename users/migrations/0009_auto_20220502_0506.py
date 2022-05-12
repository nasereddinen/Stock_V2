# Generated by Django 3.2.13 on 2022-05-02 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_demande_validation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reparation_materiel',
            name='observation',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'admin'), (2, 'user'), (4, 'superadmin')], default=4),
        ),
    ]
