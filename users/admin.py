from django.contrib import admin
from django.contrib.auth.models import Group
# Register your models here.
from .models import *
from django.contrib.admin.models import LogEntry
class famille(admin.ModelAdmin):
    list_display = ('id','famille')



admin.site.register(User)
admin.site.register(Facture)
admin.site.register(Familles)
admin.site.unregister(Group)
admin.site.register(Stock)
admin.site.register(LogEntry)
admin.site.register(SousFamille)
admin.site.register(Contact)
admin.site.register(Task)
admin.site.register(distinations)
admin.site.register(Group)
admin.site.register(reparation_materiel)
admin.site.register(Demande_Devis)
admin.site.register(Contrat)
admin.site.register(demande)
admin.site.site_header = 'interface superuser'