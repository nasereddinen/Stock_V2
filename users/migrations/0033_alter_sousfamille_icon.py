# Generated by Django 3.2.13 on 2022-07-04 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0032_alter_sousfamille_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sousfamille',
            name='icon',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]