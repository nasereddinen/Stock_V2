from typing_extensions import Self
from weakref import ref
from django.forms import ModelForm, MultipleChoiceField, widgets
from django import forms
from django.forms.formsets import formset_factory
from django.utils.translation import gettext_lazy as _
from .models import *
from django.db.models import Sum

from django.core.exceptions import ValidationError

class familleForm(ModelForm):
    def clean(self):
        famille=self.cleaned_data.get('famille')
        if Familles.objects.filter(famille=famille).exists():
            self._errors['famille'] = self.error_class(['déja exist'])
        return self.cleaned_data
    class Meta:
        model = Familles
        fields = '__all__'

class sous_familleForm(ModelForm):
    def clean(self):
        pid=self.cleaned_data.get('pid1')
        if SousFamille.objects.filter(pid1=pid).exists():
            self._errors['pid1'] = self.error_class(['déja exist'])
        return self.cleaned_data
    class Meta:
        model = SousFamille
        fields = ('id_famille','designation','marque','model','seuil','pid1','active','groupresp')
        labels = {'id_famille': _('famille'),'pid1': _('Sérial number')}
        
class sous_familleUpdateForm(ModelForm):
    class Meta:
        model = SousFamille
        fields = ('id_famille','designation','marque','model','seuil','pid1','active','groupresp','icon')
        labels = {'id_famille': _('famille'),'pid1': _('Sérial number'),'icon':_('fontawesome icon')}


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['fournisseur','nom','adresse','tel1','fax','mail','activite','ville','x','y']
    
class ContratForm(ModelForm):
    dateacquisition = forms.DateField(label="date d'aquisition",widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    echeance = forms.DateField(label="date d'eheance",widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Contrat
        fields = ['article','designation','fournisseur','dateacquisition','echeance','montant','observation','ville']
class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['id_sous_famille','quantity','reorder_level','prix']

    

class IssueForm(ModelForm):
    issue_to = forms.ModelChoiceField(queryset=distinations.objects.all(),label='Distination', empty_label='Select Distination')

    class Meta:
        model = Stock
        fields = ['issue_to']
        labels={
            'issue_to':'emplacement'
        }
class DemandeForm(forms.ModelForm):
    class Meta:
        model = demande
        fields = ['validation']
        labels = {
            'validation':'verification',
            
        }
class ReceiveForm(forms.ModelForm):
    class Meta:
        model =Stock
        fields = ['receive_quantity', 'issue_to']
        labels = {
            'receive_quantity':'quantite rendus',
            'issue_to':'rendu par'
        }
#
class factureform(forms.ModelForm):
    dateen = forms.DateField(label="date d'entre",widget=forms.widgets.DateInput(attrs={'type':'date','class':"form-control datepicker-input in-edit"}))
    bondlev = forms.FileField(required=False,widget = forms.FileInput(attrs={'class':'form-control'}))
    facture_print = forms.FileField(required=False,widget = forms.FileInput(attrs={'class':'form-control'}))

    def clean(self):
        num_fac=self.cleaned_data.get('ref')
        if Facture.objects.filter(ref=num_fac).exists():
            self._errors['ref'] = self.error_class(['déja exist'])
        return self.cleaned_data

    class Meta:
        model = Facture
        fields = ['phone_number','ref','Society','dateen','bondlev','facture_print']
        widgets={
            "bondlev": forms.FileInput(attrs={"rows": "", "class": "form-control"}),
            "facture_print": forms.FileInput(attrs={"rows": "", "class": "form-control"}),
            "dateen": forms.DateInput(attrs={"rows": "", "class": "form-control datepicker-input in-edit"}),

        }
        
class DistinationForm(forms.ModelForm):
    nom_dis = forms.CharField(required=True , label="Emplacement")
    def clean(self):
        nom_dis = self.cleaned_data.get('nom_dis')
        societe = self.cleaned_data.get('societe')
        if len(nom_dis) < 5:
            self._errors['nom_dis'] = self.error_class(['A minimum of 5 characters is required'])
        elif distinations.objects.filter(nom_dis=nom_dis,societe=societe).exists():
            self._errors['nom_dis'] = self.error_class(['déja exist'])
            self._errors['societe'] = self.error_class(['déja   exist'])
        return self.cleaned_data
    class Meta:
        model = distinations
        fields = ['nom_dis','societe']       
        
#task form
class TaskForm(forms.ModelForm):
    title = forms.CharField(widget= forms.Textarea(attrs={'placeholder':'Discription de votre Tache...'}),label='Tache')
    class Meta:
        model = Task
        fields = ['title','follows']  
        widgets={
            'follows':forms.CheckboxSelectMultiple(),
        }
        labels={
            'follows':'Partager avec'
        }
	   
        
#userform
class UserForm(ModelForm):
    username = forms.CharField(required=True , label="First Name")
    password = forms.CharField(label=_("Password"),widget=forms.PasswordInput)
    def clean(self):
        nom = self.cleaned_data.get('username')
        if User.objects.filter(username=nom).exists():
            self._errors['username'] = self.error_class(['déja exist'])
            
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username','password','role','groups']
#this for the user update
class User_Update_Form(ModelForm):
    username = forms.CharField(required=True , label="First Name")
    class Meta:
        model = User
        fields = ['username','role','groups']
#group form
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        exclude = ['permissions']
        
Formsetst = formset_factory(StockForm,extra=1)

class Devis_Form(forms.ModelForm):
  
     class Meta:
        model = Demande_Devis
        fields = ['fournisseur']
       
   



class Devis_DemandeForm(forms.ModelForm):
    class Meta:
        model = Demande_Devis
        fields = ['article','quantite']
        exclude = ['fournisseur']
    
