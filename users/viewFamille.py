from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from .form import *
from django.shortcuts import render,get_object_or_404

@login_required(login_url ='/users/login')
def famille_list(request):
    familles = Familles.objects.all()
    return render(request, 'Familypage/page_famille_list.html', {'familles': familles})

@login_required(redirect_field_name='login')
def save_famille_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            familles = Familles.objects.all()
            data['html_famille_list'] = render_to_string('Familypage/includes/famille_list.html', {
                'familles': familles
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required(redirect_field_name='login')
def famille_create(request):
    if request.method == 'POST':
        form = familleForm(request.POST)
    else:
        form = familleForm()
    return save_famille_form(request, form, 'Familypage/includes/famille_create.html')
@login_required(redirect_field_name='login')
def update_famille(request,pk):
    unfamille = Familles.objects.get(id=pk)
    if request.method == 'POST':
        form = familleForm(request.POST,instance=unfamille)
    else:
        form = familleForm(instance=unfamille)
    return save_famille_form(request, form, 'Familypage/includes/famille_update.html')


@login_required(redirect_field_name='login')
def famille_delete(request,pk):
    famille = get_object_or_404(Familles, pk=pk)
    data = dict()
    if request.method == 'POST':
        famille.delete()
        data['form_is_valid'] = True
        familles = Familles.objects.all()
        data['html_famille_list'] = render_to_string('Familypage/includes/famille_list.html',{'familles': familles})
    else:
        context = {'famille': famille}
        data['html_form'] = render_to_string('Familypage/includes/famille_delete.html',context,request=request)
    return JsonResponse(data)
 

@login_required(redirect_field_name='login')
def valid_famille_name(request):
    data= dict()
    if request.method == "POST":
        name_Famille = request.POST["id_famille"]
        data = {
        'taken':Familles.objects.filter(famille__iexact=name_Famille).exists()
        }
    return JsonResponse(data)
