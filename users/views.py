from audioop import avg
from multiprocessing import context
from this import d
from turtle import st
from venv import create
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from requests import request
from .importation import *
from django.db.models import Q
from django.contrib.auth.models import Group
from django.db.models import F
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site

def index(request):
    month = datetime.now().month
    users = get_user_model()
    Users =users.objects.all()
    rep = reparation_materiel.objects.all().count()
    dem = demande.objects.all().count()
    price= Stock.objects.all().filter(last_updated__month=month).aggregate(Sum('prix'))
    print(price)
    artcl = SousFamille.objects.all()
    tasks = Task.objects.all()
    history = Historique_Stock.objects.all()
    restant = Stock.objects.all().aggregate(Sum('quantity'))['quantity__sum']
    nb_vente=Stock.objects.values('last_updated__month').annotate(item=Sum('prix'))
    vente_month=Stock.objects.values('last_updated__month','fac__Society').annotate(item=Sum('prix')).order_by('fac__Society')
    cur_month=[]
    last_month=[]
    for vente in vente_month:
        if vente['last_updated__month'] == month:
            cur_month.append(vente)
        elif vente['last_updated__month'] == month-1:
            last_month.append(vente)
    cf = Contact.objects.all()
    nbtrans =  history.count()
    tot_articl = artcl.count()
    fourni = cf.count()
    labels = []
    data = []
    requet = Stock.objects.all()
    for societe in requet:
        labels.append(societe.id_sous_famille)
        data.append(societe.issue_quantity)
    datat=dict()
    datat['labels']=labels
    datat['series']=data
    
    lt=0
    perd=[]
    for ob in requet:
        if ob.quantity < ob.id_sous_famille.seuil:
            lt=+1
            perd.append(str(ob.id_sous_famille.designation) + " qauntité  " + str(ob.quantity - ob.id_sous_famille.seuil))
    return render(request, "./home/index.html",{"prix":price,'vente_month':cur_month,'vente_lastmth':last_month,
    "trans":str(nbtrans),"labels":labels,"data":datat,"alert":lt,"list":perd,"stck":requet,
    "rest":restant,"nbfour":fourni,"Stock":requet,"nbarticle":tot_articl,
    'tasks':tasks,"allusers":Users,'nb_dem':dem,'nb_rep':rep,'page_name':'dashboard','vente':nb_vente})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "./home/page-sign-in.html", {
                "message": "Invalid credentials."
            })
    else:
        return render(request, "./home/page-sign-in.html")


def logout_view(request):
    logout(request)
    return render(request, "./home/page-sign-in.html", {
        "message": "Logged out."
    })
@login_required(redirect_field_name='login')
def sous_famille(request):
     if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
     form = familleForm()
     return render(request,"./ArticlePage/articles.html",{
         'sous_famille':SousFamille.objects.all(),
         "form":form,
         'page_name':'list des articles'
     })
@login_required(redirect_field_name='login')
def article_form(request):
    form = sous_familleForm()
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
         form = sous_familleForm(request.POST)
         if form.is_valid():
             form.save()
             return HttpResponseRedirect(reverse("article"))
    return render(request,"./ArticlePage/form.html",{
         "page_name":'Ajouter Article',
         "form":form
    })

@login_required(redirect_field_name='login')
def articleUpdate(request,pk):
    instance = get_object_or_404(SousFamille, id=pk)
    if request.method == "POST":
        artcl_form = sous_familleUpdateForm(request.POST or None,instance=instance)
        if artcl_form.is_valid():
            artcl_form.save()
            return HttpResponseRedirect(reverse("article"))
    else:
        artcl_form = sous_familleUpdateForm(instance=instance)
    return render(request,"./ArticlePage/form.html",{'form':artcl_form,'page_name':'Edit Article'})

@login_required(redirect_field_name='login')
def articledelete(request,pk):
    Sousfamille = SousFamille.objects.get(id=pk)
    if request.method == 'POST':
        Sousfamille.delete()
        return HttpResponseRedirect(reverse("article"))
    return render(request,"/ArticlePage/articles.html",{"artcl":Sousfamille,'page_name':'supprimer article'})

@login_required(redirect_field_name='login')
def fournisseur(request):
    form = ContactForm()
    
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
        form =ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("fornisseur"))
    
    return render(request,"./FournisseurPage/fournisseur.html",{
         'fornisseur':Contact.objects.all(),
         "form":form,
         'page_name':'fournisseur'
     })     
@login_required(redirect_field_name='login')
def contrat(request):
     list_contrat=Contrat.objects.all()
     return render(request,"./PageContrat/contrat.html",{'contrats':list_contrat,'page_name':'contrat'}) 
@login_required
def updateContrat(request, pk):
	task = Contrat.objects.get(id=pk)
	form = ContratForm(instance=task)
	if request.method == 'POST':
		form = ContratForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse("Contrat"))
	context = {'form':form,'page_name':'update contrat'}
	return render(request, 'PageContrat/contratForm.html', context)

@login_required(redirect_field_name='login')
def deleteContrat(request, pk):
	item = Contrat.objects.get(id=pk)
	if request.method == 'POST':
		item.delete()
		return HttpResponseRedirect(reverse("Contrat"))
	context = {'item':item,'page_name':'Supprimer Contrat'}
	return render(request, 'PageContrat/contrat.html', context)

@login_required(redirect_field_name='login')
def stock_ajout(request):
    if request.method == 'GET':
        formset = Formsetst(request.GET or None)
        formi = factureform(request.GET or None)
    elif request.method == 'POST':
        formset = Formsetst(request.POST)
        formi = factureform(request.POST,request.FILES)
        if formi.is_valid():
            facutre = Facture.objects.create(phone_number_id=formi.data["phone_number"],ref=formi.data["ref"],Society=formi.data["Society"],dateen=formi.data['dateen'])
        else:
            return HttpResponse(' ref doit etre unique')
        if formset.is_valid():
            try:
                distination = distinations.objects.get(nom_dis="stock")
            except distinations.DoesNotExist:
                distination = distinations(societe='autre',nom_dis="stock")
                distination.save()
            for form in formset:
                famil = form.cleaned_data.get('id_sous_famille')
                quan = form.cleaned_data.get('quantity')
                garantie=form.cleaned_data.get('reorder_level')
                prix=form.cleaned_data.get('prix')
                
                if(famil.active == 'oui'):
                     Stock(id_sous_famille=famil,quantity=quan,reorder_level=garantie,issue_to = distination,fac=facutre,ci='consommable',prix=prix).save()
                else:
                    for i in range(0,quan):
                        code=str(form.cleaned_data.get('id_sous_famille'))[0:5] + str(famil.id) + str(i)+str(i+1)+str(quan)+str(facutre.id)
                        instance=Stock(id_sous_famille=famil,
                        quantity=1,
                        issue_quantity=0,
                        receive_quantity=0,
                        reorder_level=garantie,
                        fac=facutre,
                        ci=code,
                        issue_to=distination,
                        prix=prix)
                        instance.save()
                        entre_history=Historique_Stock(last_updated = instance.last_updated,id_sous_famille = instance.id_sous_famille,quantity = instance.quantity, receive_quantity = instance.receive_quantity, receive_by = instance.receive_by, issue_to = instance.issue_to,ci = instance.id,codeibar=instance.ci)
                        entre_history.save()
            
            return HttpResponseRedirect(reverse('stock_details'))
    return render(request,"./PageStock/AjouterStock.html",{"formset":formset,"form":formi,"page_name":"ajouter stock"})

@login_required(redirect_field_name='login')
def stock_details(request):
    liste_article = Stock.objects.all()
    nb_fac=Stock.objects.values('fac__ref','fac__id','fac__dateen','fac__bondlev','fac__facture_print').annotate(item=Sum(F('issue_quantity')+F('quantity'))).order_by('fac__dateen')
    if request.method == "POST":
        item_id= request.POST["item"]
        item=Stock.objects.get(id=item_id)
        nb_fac=Stock.objects.values('fac__ref','fac__id','fac__dateen','fac__bondlev','fac__facture_print').annotate(item=Sum(F('issue_quantity')+F('quantity'))).order_by('fac__dateen')
        nb_fac = nb_fac.filter(fac__ref=item.fac.ref)
    return render(request,"./PageStock/stock_delais.html",{'page_name':'Facturation','Stock':nb_fac,'liste_article':liste_article})    

@login_required(redirect_field_name='login')
def receive_items(request, pk):
    queryset=Stock.objects.get(id=pk)
    if request.method == 'GET':
         form=ReceiveForm(request.GET or None,instance=queryset,initial={'receive_quantity':1})
         if(queryset.ci != 'consommable'):
            form.fields['receive_quantity'].widget.attrs['readonly']= True
    if request.method == 'POST':
        form=ReceiveForm(request.POST, instance=queryset or None)
      
    if form.is_valid():
        instance=form.save(commit=False) 
        if  instance.receive_quantity > instance.issue_quantity:
            return HttpResponse("quantity problem")
        instance.quantity += instance.receive_quantity
        instance.receive_quantity = instance.receive_quantity
        instance.issue_quantity = instance.issue_quantity - instance.receive_quantity
        instance.receive_by = request.user
        instance.issue_to = distinations.objects.get(nom_dis='stock')
        instance.save()
        issue_history = Historique_Stock(last_updated = instance.last_updated,id_sous_famille = instance.id_sous_famille,quantity = instance.quantity, receive_quantity = instance.receive_quantity, receive_by = instance.receive_by, issue_to = instance.issue_to,ci = instance.id,codeibar=instance.ci)
        issue_history.save()
        return HttpResponseRedirect(reverse('stock_details'))
    context = {
			"title": 'Reaceive ' + str(queryset.id_sous_famille),
			"instance": queryset,
			"form": form,   
			"username": 'Recu a: ' + str(request.user),
            'page_name':'retour stock'
            }
	
    return render(request, "./PageStock/receive_form.html", context)

@login_required(redirect_field_name='login')
def chaque_detail(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"title": queryset.id_sous_famille,
		"queryset": queryset,
	}
	return render(request, "./PageStock/chaque.html", context)

@login_required(redirect_field_name='login')
def issue_items(request, pk):
    queryset=Stock.objects.get(id=pk)
    form=IssueForm()
    alertquery = Stock.objects.filter(issue_to__nom_dis='stock').values('id_sous_famille__id','id_sous_famille__designation','id_sous_famille__seuil','id_sous_famille__marque').annotate(total_qt=Sum('quantity'))
    alertmail=[]
    for qt in alertquery:
        if qt['total_qt'] < qt['id_sous_famille__seuil']:
            alertmail.append(qt)
            article=SousFamille.objects.get(id=qt['id_sous_famille__id'])
            article_ext=Demande_Devis.objects.filter(article=article).exists()
            if article_ext:
                demande_devis=Demande_Devis.objects.get(article=article)
                demande_devis.quantite=qt['total_qt']
                demande_devis.avg=int(qt['total_qt']-qt['id_sous_famille__seuil'])
                demande_devis.save()
            else:
                Demande_Devis(article=article,quantite=qt['total_qt'],avg=int(qt['total_qt']-qt['id_sous_famille__seuil'])).save()
  
    html_content = render_to_string('Pdf_templates/mail_template.html', {'list':alertquery,'alter':alertmail,'domain':request.get_host()}) 
    text_content = strip_tags(html_content) 
    email_from = settings.EMAIL_HOST_USER
    user_group = queryset.id_sous_famille.groupresp  
    group=Group.objects.get(id=user_group.id)
    email_to=group.email
# create the email, and attach the HTML version as well.
    subject=' alert seuil'
    msg = EmailMultiAlternatives(subject, text_content, email_from, [email_to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    if request.method == 'POST':
        form=IssueForm(request.POST, instance=queryset)
        issue_qt = int(request.POST['issue_quantity'])
    if form.is_valid() and issue_qt <= queryset.quantity:
        instance=form.save(commit=False)
        instance.quantity -= int(request.POST['issue_quantity'])
        instance.issue_quantity = instance.issue_quantity + int(request.POST['issue_quantity'])
        instance.issue_by=request.user
        instance.save()
        messages.success(request, "affecter SUCCESS. " + str(instance.quantity) + " " + str(instance.id_sous_famille) + "est on stock")
        issue_history = Historique_Stock(
	    last_updated = instance.last_updated,
	    id_sous_famille = instance.id_sous_famille,
	    quantity = instance.quantity, 
	    issue_quantity = int(request.POST['issue_quantity']), 
	    issue_by = instance.issue_by, 
        issue_to = instance.issue_to, 
        ci = instance.id,
        codeibar=instance.ci)
        issue_history.save()
        alertquery = Stock.objects.filter(issue_to__nom_dis='stock').values('id_sous_famille__designation','id_sous_famille__marque').annotate(total_qt=Sum('quantity'))
        
                   
        return HttpResponseRedirect(reverse('stock_details'))

    context = {
			"title": 'Reaceive ' + str(queryset.id_sous_famille),
			"instance": queryset,
			"form": form,
			"username": 'Recu a: ' + str(request.user),
            'alter':alertquery,
            'test':alertmail,
            'page_name':'affectation de materiel',
            }
    return render(request, "./PageStock/issue_form.html", context)
#################### Gest Devis ########################
@login_required(redirect_field_name='login')
def Demande_devis(request):
    demandes=Demande_Devis.objects.all().filter(avg__lte=0)
    frns=Contact.objects.all()
    FormsetDevis = modelformset_factory(Demande_Devis,form=Devis_DemandeForm,extra=0)
    if request.method == "GET":
        fournisseurs= Devis_Form(request.GET or None)
        formset = FormsetDevis(request.GET or None, queryset=demandes)
    else:
        formset = FormsetDevis(request.POST or None, queryset=demandes)
        fournisseurs = Devis_Form(request.POST or None)
        societe = request.POST['societe']
        if all([fournisseurs.is_valid(),formset.is_valid()]):
            list_fournisseur = request.POST.getlist("fournisseurs")
            
            print(list_fournisseur)
            message = ""
            for form in formset:
                message+=str(form.cleaned_data['quantite']) + ' * ' +str(form.cleaned_data['article'])+'\n'
            print(message)
            for mail in list_fournisseur:
                mailto = Contact.objects.get(id=mail)
                email_from = settings.EMAIL_HOST_USER
                try:
                    send_mail("demande de devis ",str('Bonjour ,\n'+'Merci d\'envoyer un devis sous le nom de la societe '+societe+'\n'+message),email_from,[str(mailto.mail)])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.') 
    context={'formset':formset,'F_form':fournisseurs,'list_fournisseur':frns,'page_name':'demande de devis'}
    return render(request,"./PageContrat/demande_devis.html",context)
###################### add contrat ######################
@login_required(redirect_field_name='login')  
def ajoutContrat(request):
    form = ContratForm()
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
        form =ContratForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("Contrat"))
    return render(request,"./PageContrat/contratForm.html",{"form":form,'page_name':'Ajouter Contrat'}) 

@login_required(redirect_field_name='login')  
def fournisseurmap(request,pk):
    fournisseur =  Contact.objects.get(id=pk)
    context={"fournisseur":fournisseur,'page_name':'map fournisseur'}
    return render(request,"./PageContrat/fournisseur_distance.html",context) 
############### Historique ###############
@login_required(redirect_field_name='login')
def Historique(request):
	queryset = Historique_Stock.objects.all()
	context = {"queryset": queryset,'page_name':'Historique'}
	return render(request, "./PageStock/historique.html", context)

@login_required(redirect_field_name='login')
def retour_details(request):
    tous_article = Stock.objects.filter(~Q(issue_to__nom_dis='stock'),issue_quantity__gt=0)
    filtrer = ArticleFilter(request.GET,queryset=tous_article)
    s=filtrer.qs.aggregate(Sum('quantity'))['quantity__sum']
    list_article = filtrer.qs
    return render(request,"./PageStock/retour_delais.html",{'Stock':list_article,'filtrer':filtrer,'titre':s,'page_name':'retour stock'})   

@login_required(redirect_field_name='login')
def gest_Distinations(request):
    distination = distinations.objects.all()
    context={'emplacement':distination,'page_name':'emplacement'}
    return render(request,"./PageDistination/Distinations.html",context)

@login_required(redirect_field_name='login')
def add_Distinations(request):
    Dis_Form = DistinationForm(None)
    if request.method == 'POST':
        Dis_Form = DistinationForm(request.POST)
        
        if Dis_Form.is_valid():
            Dis_Form.save()
            return HttpResponseRedirect(reverse("gest_Distinations"))
    context={'form':Dis_Form,'page_name':'Ajouter Distination'}
    return render(request,"./PageDistination/DistinationForm.html",context)


@login_required(redirect_field_name='login')
def DistinationUpdate(request,pk):
    emp = distinations.objects.get(id=pk)
    form = DistinationForm(instance=emp)
    if request.method == "POST":
        form = DistinationForm(request.POST,instance=emp)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("gest_Distinations"))
    return render(request,"./PageDistination/DistinationForm.html",{"form":form,'page_name':'Update Distination'})

@login_required(redirect_field_name='login')
def deleteDistination(request,pk):
    emp = distinations.objects.get(id=pk)
    if request.method == 'POST':
        emp.delete()
        return HttpResponseRedirect(reverse("gest_Distinations"))
    return render(request,"./PageDistination/Distinations.html",{"distination":emp,'page_name':'Delete Distination'})
#########################----------BARCODE-----------------------#################
@login_required(redirect_field_name='login')
def chaque_Barcode(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"title": queryset.id_sous_famille,
		"queryset": queryset,
        'page_name':'Code A Bar'
	}
	return render(request, "./PageStock/Barcode.html", context)

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    pdf_status = pisa.CreatePDF(html, dest=response)

    if pdf_status.err:
        return HttpResponse('Some errors were encountered <pre>' + html + '</pre>')
    return response

@login_required(redirect_field_name='login')
def pdf_view(request, pk):
    template_name = './Pdf_templates/template_facture.html'
    facture_details = Facture.objects.get(id=pk)
    items = Stock.objects.filter(fac__id=pk)
    context = {"ref": facture_details.ref,"societe": facture_details.Society,"date":facture_details.dateen,"fournisseurnom":facture_details.phone_number.nom,"fournisseurmail":facture_details.phone_number.mail,"fac_id": facture_details.id, "items":items}
    return render_to_pdf(template_name,context)
@login_required(redirect_field_name='login')
def facture_view(request, pk):
    template_name = './Pdf_templates/viewTemplate.html'
    facture_details = Facture.objects.get(id=pk)
    items = Stock.objects.filter(fac__id=pk)
    context = {"ref": facture_details.ref,"societe": facture_details.Society,"date":facture_details.dateen,"fournisseurnom":facture_details.phone_number.nom,"fournisseurmail":facture_details.phone_number.mail,"fac_id": facture_details.id, "items":items}
    return render(request,template_name,context)

@login_required(redirect_field_name='login')
def histbyown(request):     
    data = Historique_Stock.objects.all().values('ci','id_sous_famille__designation','codeibar','id_sous_famille__model').distinct()
    return render(request, "./PageStock/listhistory.html", {"data":data})

@login_required(redirect_field_name='login')
def itemhistory(request,pk):     
    infos=Historique_Stock.objects.filter(ci=pk)[0]
    data = Historique_Stock.objects.filter(ci=pk)
    return render(request, "./PageStock/itemhistory.html", {"data":data,"infos":infos})

@login_required(redirect_field_name='login')
def item_history_pdf(request,pk): 
    template_name = './Pdf_templates/template_history_item_pdf.html' 
    infos=Historique_Stock.objects.filter(ci=pk)[0]
    data = Historique_Stock.objects.filter(ci=pk)
    context = {"data":data,"infos":infos}
    return render_to_pdf(template_name,context)

#todo goes there===>:

@login_required(redirect_field_name='login')
def List_tasks(request):
    tasks = Task.objects.all().order_by('created')
    p = Paginator(tasks, 3)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    context = {'tasks':tasks, 'form':form,'page_obj':page_obj,'name_page':'Tache'}
    return render(request, 'todos/list.html', context)

@login_required(redirect_field_name='login')
def task_form(request):
    form = TaskForm()
    form.fields['follows'].queryset = User.objects.filter(groups=request.user.groups.all().first())
    if request.method =='POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task=form.save()
            task.by=request.user.username
            task.save()
            return HttpResponseRedirect(reverse("list_tasks"))
    context = {'form':form,'name_page':'Ajouter Tache'}
    return render(request,'todos/todo_form.html',context)
@login_required(redirect_field_name='login')
def List_Voice_tasks(request):
    context={}
    return render(request, 'todos/list_voix.html', context)
@login_required(redirect_field_name='login')
def updateTask(request, pk):
	task = Task.objects.get(id=pk)
	form = TaskForm(instance=task)
	if request.method == 'POST':
		form = TaskForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse("list_tasks"))
	context = {'form':form,'name_page':'Edit Tache'}
	return render(request, 'todos/list.html', context)
@login_required(redirect_field_name='login')
def deleteTask(request,pk):
	item = Task.objects.get(id=pk)
	item.delete()
	return HttpResponseRedirect(reverse("list_tasks"))
	
def cross_on(request,pk):
    item=Task.objects.get(id=pk)
    item.complete=True
    item.save()
    return HttpResponseRedirect(reverse("list_tasks"))

def cross_off(request,pk):
    item=Task.objects.get(id=pk)
    item.complete=False
    item.save()
    return HttpResponseRedirect(reverse("list_tasks"))

### sortie stock #######
@login_required(redirect_field_name='login')
def Sortie_stock(request):
    tous_article = Stock.objects.all().filter(quantity__gt = 0,issue_to__nom_dis='stock')
    if request.method == 'GET':
        filtrer_gat = request.GET.get('filter_gat')
        if filtrer_gat != '' and filtrer_gat is not None:
            tous_article = tous_article.filter(id_sous_famille__active=filtrer_gat)
    s=tous_article.aggregate(Sum('quantity'))['quantity__sum']
    ms = dumps(s)
    context={'list_article':tous_article,"ms":ms,'name_page':'sortie stock'}
    return render(request,"./PageStock/Sortie_Stock.html",context)
############## gestion user ##################
@login_required(redirect_field_name='login')
def users_view(request):
    users_list = User.objects.values()
    context = {'list_users':users_list,'page_name':'Utilisateurs'}
    return render(request,"./PageUser/users_list.html",context)
@login_required(redirect_field_name='login')
def add_user(request):
    if request.method == "GET":
        form = UserForm(request.GET or None)
    elif request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            role = form.cleaned_data.get('role')
            user = User.objects.create_user(username=username,password=password,is_staff=False,is_active=True)
            user.set_password(password)
            user.save()
            if role == 1:
                techgroup = Group.objects.get_or_create(name='tech')
                techgroup[0].user_set.add(user)
                user.is_staff = True
                user.save()
            if role == 2:
                comptagroup = Group.objects.get_or_create(name='comptabiliter')
                comptagroup[0].user_set.add(user)
                user.is_staff = False
                user.save()
            elif role == 4:
                superadmingroup = Group.objects.get_or_create(name='superadmin')
                superadmingroup[0].user_set.add(user)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            elif role == 3:
                managergroup = Group.objects.get_or_create(name='managers')
                managergroup[0].user_set.add(user)
                user.is_staff = False
                user.save()
            return HttpResponseRedirect(reverse("users"))
    return render(request,"./PageUser/users_form.html",{"form":form,'page_name':'Ajouter utilisateur'})

@login_required(login_url ='/login')
def update_user(request,pk):
    use =User.objects.get(id=pk)
    form = User_Update_Form(instance=use)
    if request.method == "POST":
        form = User_Update_Form(request.POST,instance=use)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            print(role)
            if role == 4:
                use.is_staff = True
                use.is_superuser = True
                use.save()
            elif role==1:
                use.is_staff = True
                use.save()
            elif role==2:
                use.is_staff = False
                use.is_superuser = False
                use.save()
            
            return HttpResponseRedirect(reverse("users"))
    return render(request,"./PageUser/users_form.html",{"form":form,'page_name':'Edit utilisateur'})
@login_required(redirect_field_name='login')
def deleteUser(request, pk):
	user = User.objects.get(id=pk)
	user.is_active = False
	user.save()
	return HttpResponseRedirect(reverse("users"))
#list_groupe
@login_required(login_url ='/login')
def groups_view(request):
    groups_list = Group.objects.all()
    context = {'list_groups':groups_list,'page_name':'Groups'}
    return render(request,"./PageUser/groups_list.html",context)

#add_groupe
@login_required(login_url ='/login')
def add_groupe(request):
    form = GroupForm()
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("groups"))
    return render(request,"./PageUser/groups_form.html",{"form":form,'page_name':'Ajouter Group'})

@login_required(login_url ='/login')
def update_group(request,pk):
    group = Group.objects.get(id=pk)
    form = GroupForm(instance=group)
    if request.method == "POST":
        form = GroupForm(request.POST,instance=group)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("groups"))
    return render(request,"./PageUser/groups_form.html",{"form":form,"page_name":'Edit Group'})

@login_required(redirect_field_name='login')
def listproduct(request):
    list_famille= Familles.objects.all()
    listproduct = Stock.objects.filter(issue_to__nom_dis='stock').values('id_sous_famille__designation','id_sous_famille__icon','id_sous_famille__designation').annotate(total_qt=Sum('quantity'))
    if request.method == 'POST':
        cat = request.POST['category']
        listproduct = Stock.objects.filter(issue_to__nom_dis='stock',id_sous_famille__id_famille=cat).values('id_sous_famille__designation','id_sous_famille__designation').annotate(total_qt=Sum('quantity'))
    context = {'listProducts':listproduct,'list_famille':list_famille,'page_name':'Les Produits'}
    return render(request,"./demandes/demander_produit.html",context)

@login_required(redirect_field_name='login')
def listdemandes(request):
    listdemande = demande.objects.all()
    context = {'listdemandes':listdemande,'page_name':'Demandes'}
    return render(request,"./demandes/verification_demande.html",context)

@login_required(redirect_field_name='login')
def save_demande_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            qt = request.POST["quantite_livred"]
            etat=form.cleaned_data.get('validation')
            emp = request.POST["emplacement"]
            if etat != 'valider':
                form.save()
                data['form_is_valid'] = True
            else:
                demand=form.save(commit=False)
                st_qt=demand.article.quantity
                email_from = settings.EMAIL_HOST_USER
                user_group = demand.demander.groups.all().first()
                print(user_group)
                group=Group.objects.get(id=user_group.id)
                email_to=group.email
                if(int(qt)>st_qt):
                    data['form_is_valid'] = False
                    data['quantite_invalid'] = True
                else:
                    demand.quantite=qt
                    demand.save()
                    demande_distination= distinations.objects.get(id=emp)
                    instance_stock = Stock.objects.get(id=demand.article.id)
                    instance_stock.quantity -= int(qt)
                    instance_stock.issue_quantity = instance_stock.issue_quantity + int(qt)
                    instance_stock.issue_by=request.user
                    instance_stock.issue_to=demande_distination
                    instance_stock.save()
                    issue_history = Historique_Stock(last_updated = instance_stock.last_updated,id_sous_famille = instance_stock.id_sous_famille,quantity = instance_stock.quantity, issue_quantity = int(qt), issue_by = instance_stock.issue_by, issue_to = instance_stock.issue_to, ci = instance_stock.id,codeibar=instance_stock.ci)
                    issue_history.save()
                    try:
                        send_mail("demande materiel", " demande de "+str(demand.article.id_sous_famille.designation)+" valider Par "+str(request.user),email_from,[email_to])
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    data['form_is_valid'] = True
            listdemandes = demande.objects.all()
            data['html_demande_list'] = render_to_string('demandes/liste_demandes.html', {
                'listdemandes':listdemandes
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form,"destinations":distinations.objects.all()}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
@login_required(redirect_field_name='login')
def verifier_demandes(request,pk):
    dem=demande.objects.get(id=pk)
    if request.method == 'POST':
        form = DemandeForm(request.POST or None,instance=dem)
    else:
        form = DemandeForm(instance=dem)
    return  save_demande_form(request, form, './demandes/verification_demande_modal.html')
@login_required(redirect_field_name='login')
def demande_product(request,pk):
    article = Stock.objects.filter(id_sous_famille__designation=pk)
    getarticle = Stock.objects.get(id=article[0].id)
    if request.method == "POST":
        quantite = request.POST[pk]
        if quantite:
            demande.objects.create(article = article[0],demander = request.user,quantite = quantite)
            email_from = settings.EMAIL_HOST_USER
            email_to = str(getarticle.id_sous_famille.groupresp.email)
            
            try:
                send_mail("demande materiel", "Par "+str(request.user)+" demande de "+str(getarticle.id_sous_famille.designation)+"  quantiter: "+str(quantite),email_from,[email_to])
            except BadHeaderError:
                return HttpResponse('Invalid header found.') 
    return HttpResponseRedirect(reverse("list_product"))
    
@login_required(redirect_field_name='login')
def list_reparated(request):
    list_rep = Stock.objects.all()
    em=['case','stock','reparation']
    for e in em:
        list_rep = list_rep.filter(~Q(issue_to__nom_dis=e))
    context={'list_rep':list_rep,'page_name':'reparation'}
    return render(request,"./demandes/demande_reparation.html",context)


@login_required(redirect_field_name='login')
def demande_reparation(request,pk):
    item = Stock.objects.get(id=pk)
    if request.method == "POST":
        observation = request.POST['observation']                                      
        reparation_materiel(article=item,demander=request.user,observation=observation,etat='en-cours').save()
        email_from = settings.EMAIL_HOST_USER
        email_to = str(item.id_sous_famille.groupresp.email)
        print(email_to)
        try:      
            send_mail("reparation materiel", "Par "+str(request.user)+" demande la reparation  de "+str(item.id_sous_famille.designation)+"  code: "+item.ci,email_from,[email_to])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect(reverse("list_reparation"))
    context={'item':item,'name_page':'Demande reparation'}
    return render(request,"./demandes/reparation_form.html",context)

@login_required(redirect_field_name='login')
def list_demande_reparation(request):
    mot_etat='en cours'
    if not (request.user.groups == 'tech' or request.user.is_staff == True): 
        return HttpResponse('you don t have access to')
    else:
        if request.method == 'POST':
            etat = request.POST['etat']
            mot_etat=etat
            list_reclamation = reparation_materiel.objects.filter(etat=etat)
        else:
            list_reclamation = reparation_materiel.objects.all()     
    context={'list_recla':list_reclamation,'titre_etat':mot_etat,'page_name':'Demande reparation'}
    return render(request,"./demandes/list_reparation.html",context)

@login_required(redirect_field_name='login')
def verfication_reparation(request,pk):
    reclamation = reparation_materiel.objects.get(id = pk)
    item = Stock.objects.get(id=reclamation.article.id)
    list_emp = Historique_Stock.objects.filter(codeibar=item.ci)
    if request.method == 'POST':
        etat = request.POST['etat']
        emp_his = request.POST['emp_his']
        reclamation.etat = etat
        reclamation.save()
        if etat == 'case':
            emplacement,created = distinations.objects.get_or_create(nom_dis='case')
            item = Stock.objects.get(id=reclamation.article.id)
            item.issue_to=emplacement
            item.issue_by = str(request.user)
            item.save()
            issue_history = Historique_Stock(last_updated = item.last_updated,id_sous_famille = item.id_sous_famille,quantity = item.quantity, receive_quantity = item.receive_quantity, receive_by = item.receive_by, issue_to = item.issue_to,issue_by = item.issue_by,ci = item.id,codeibar=item.ci)
            issue_history.save()
        elif etat =='en-cours':
            emplacement,created = distinations.objects.get_or_create(nom_dis='reparation')
            item = Stock.objects.get(id=reclamation.article.id)
            item.issue_to=emplacement
            item.issue_by = request.user
            item.save()
            issue_history = Historique_Stock(last_updated = item.last_updated,id_sous_famille = item.id_sous_famille,quantity = item.quantity, receive_quantity = item.receive_quantity, receive_by = item.receive_by, issue_to = item.issue_to,ci = item.id,issue_by = item.issue_by,codeibar=item.ci)
            issue_history.save()
        elif etat == "resolu":
            print("resolu")
            item = Stock.objects.get(id=reclamation.article.id)
            emp=distinations.objects.get(id=emp_his)
            item.issue_to=emp
            item.save()
            issue_history = Historique_Stock(last_updated = item.last_updated,id_sous_famille = item.id_sous_famille,quantity = item.quantity, receive_quantity = item.receive_quantity, receive_by = item.receive_by, issue_to = item.issue_to,ci = item.id,issue_by = item.issue_by,codeibar=item.ci)
            issue_history.save()
        return HttpResponseRedirect(reverse('list_reclamation'))

    context={"reclamation":reclamation,"list_emp":list_emp}
    return render(request,"./demandes/verification_reparation.html",context)
@login_required(redirect_field_name='login')
def emplacement_societe(request):
    items = Stock.objects.filter(issue_quantity__gt=0)
    distination = distinations.objects.all()
    reclamation=reparation_materiel.objects.filter(etat='en-cours')
    nb_dis=distinations.objects.values('societe').annotate(Count('societe')).order_by().filter(societe__count__gte=1)
    nb_items=Stock.objects.values('issue_to__societe').annotate(Count('id'))
    context = {'items':items,'distinations':distination,'soc_prod':nb_dis,'all':nb_items,'rec':reclamation,'page_name':'emplacement'}
    return render(request,"./PageDistination/societe_emplacement.html",context)

@login_required(redirect_field_name='login')
def items_Distinations(request,pk):
    items = Stock.objects.all().filter(issue_quantity__gt=0,issue_to__societe=pk,id_sous_famille__active='non')
    distination = distinations.objects.filter(societe=pk)
    reclamation = reparation_materiel.objects.filter(etat='en-cours')
    context = {'items':items,'distinations':distination,'rec_item':reclamation}
    return render(request,"./PageDistination/item_emplacement.html",context)

@login_required(redirect_field_name='login')
def box_details(request,pk):
    items = Stock.objects.filter(issue_quantity__gt=0,issue_to__id=pk,id_sous_famille__active='non')
    distination = distinations.objects.get(id=pk)
    reclamation=reparation_materiel.objects.filter(etat='en-cours')
    context = {'items':items,'distination':distination,'rec':reclamation,'page_name':'detail box'}
    return render(request,"./PageDistination/box_details.html",context)

@login_required(redirect_field_name='login')
def emplacement_autre(request):
    items = Stock.objects.filter(issue_quantity__gt=0)
    distination = distinations.objects.all()
    reclamation=reparation_materiel.objects.filter(etat='en-cours')
    nb_dis=distinations.objects.values('societe').annotate(Count('societe')).order_by().filter(societe__count__gte=1)
    context = {'items':items,'distinations':distination,'soc_prod':nb_dis,'rec':reclamation}
    return render(request,"./PageDistination/autre_emplacement.html",context)
