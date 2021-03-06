# Generated by Django 3.2.13 on 2022-05-30 02:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_alter_contact_fournisseur'),
    ]

    operations = [
        migrations.AddField(
            model_name='facture',
            name='bondlev',
            field=models.FileField(blank=True, null=True, upload_to='media/bon_livraison'),
        ),
        migrations.AddField(
            model_name='facture',
            name='facture_print',
            field=models.FileField(blank=True, null=True, upload_to='media/facture'),
        ),
        migrations.AddField(
            model_name='stock',
            name='prix',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='historique_stock',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='HisCreatUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='historique_stock',
            name='id_sous_famille',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.sousfamille'),
        ),
        migrations.AlterField(
            model_name='historique_stock',
            name='issue_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='hisIssueUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='historique_stock',
            name='issue_to',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.distinations', verbose_name='Emplacement'),
        ),
        migrations.AlterField(
            model_name='historique_stock',
            name='receive_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='hisReceiveUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='stock',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='CreatUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='stock',
            name='issue_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='IssueUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='stock',
            name='receive_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ReceiveUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
