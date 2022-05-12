

from django.forms import ModelForm, widgets
from django import forms
from django.forms.formsets import formset_factory
from django.utils.translation import gettext_lazy as _
from .models import *
from django.core.exceptions import ValidationError


class familleForm(ModelForm):
     
    class Meta:
        model = Familles
        fields = '__all__'

class sous_familleForm(ModelForm):
    class Meta:
        model = SousFamille
        fields = ('id_famille','designation','marque','model','seuil','pid1','active','groupresp')
        labels = {
            'id_famille': _('famille'),
            'pid1': _('Sérial number')
        }



class ContactForm(ModelForm):
    
    class Meta:
        model = Contact
        fields = ['fournisseur','nom','adresse','tel1','fax','mail','activite','ville']
class ContratForm(ModelForm):
    dateacquisition = forms.DateField(label="date d'aquisition",widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    echeance = forms.DateField(label="date d'eheance",widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Contrat
        fields = ['article','designation','fournisseur','dateacquisition','echeance','montant','observation','ville']
class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['id_sous_famille','quantity','reorder_level']
       
    
    def __init__(self, *args,**kwargs):
        super(StockForm, self).__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
 
        
class IssueForm(ModelForm):
    issue_to = forms.ModelChoiceField(queryset=distinations.objects.all(),label='Distination', empty_label='Select Distination')

    class Meta:
        model = Stock
        fields = ['issue_to']
        labels={
            'issue_to':'emplacement'
        }
  

class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['receive_quantity', 'issue_to']
        labels = {
            'receive_quantity':'quantite rendus',
            'issue_to':'rendu par'
        }
   
#
class fornisseurform(forms.ModelForm):
    dateen = forms.DateField(label="date d'entre",widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Facture
        fields = ['phone_number','ref','Society','dateen']
        
class DistinationForm(ModelForm):
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