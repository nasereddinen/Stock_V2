from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from .form import *
from django.shortcuts import render,get_object_or_404

@login_required(redirect_field_name='login')
def fournisseur_main(request):
    frns = Contact.objects.all()
    return render(request, 'FournisseurPage/fournisseur_main.html', {'fournisseurs': frns})

@login_required(redirect_field_name='login')
def save_fournisseur_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            frns = Contact.objects.all()
            data['html_fournisseur_list'] = render_to_string('FournisseurPage/includes/fournisseur_list.html', {
                'fournisseurs': frns
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required(redirect_field_name='login')
def create_fournisseur(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
    else:
        form = ContactForm()
    return save_fournisseur_form(request, form, 'FournisseurPage/includes/fournisseur_create.html')

@login_required(redirect_field_name='login')
def update_fournisseur(request,pk):
    unfrn = Contact.objects.get(id=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST,instance=unfrn)
    else:
        form = ContactForm(instance=unfrn)
    return save_fournisseur_form(request, form, 'FournisseurPage/includes/fournisseur_update.html')


@login_required(redirect_field_name='login')
def delete_fournisseur(request,pk):
    fournisseur = get_object_or_404(Contact, pk=pk)
    data = dict()
    if request.method == 'POST':
        fournisseur.delete()
        data['form_is_valid'] = True
        fournisseur = Contact.objects.all()
        data['html_fournisseur_list'] = render_to_string('FournisseurPage/includes/fournisseur_list.html',{'fournisseurs': fournisseur})
    else:
        context = {'fournisseur': fournisseur}
        data['html_form'] = render_to_string('FournisseurPage/includes/fournisseur_delete.html',context,request=request)
    return JsonResponse(data)
 


