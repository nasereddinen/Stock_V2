from multiprocessing import context
from turtle import st
from venv import create

from requests import request
from .importation import *
from django.db.models import Q
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
@login_required(login_url ='/login')
def index(request):
    
    users = get_user_model()
    Users =users.objects.all()
    rep = reparation_materiel.objects.all().count()
    dem = demande.objects.all().count()
    price= Stock.objects.all().aggregate(Sum('issue_quantity'))['issue_quantity__sum']
    artcl = SousFamille.objects.all()
    tasks = Task.objects.all()
    history = Historique_Stock.objects.all()
    restant = Stock.objects.all().aggregate(Sum('quantity'))['quantity__sum']
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
            ###engine = pyttsx3.init()
            ##engine.setProperty("rate", 148)
            #engine.setProperty('volume',1.0) 
            #engine.say("attention il ya " + (str(ob.id_sous_famille.designation) + " qauntité  " + str(ob.quantity - ob.id_sous_famille.seuil)))
            #engine.runAndWait()
            perd.append(str(ob.id_sous_famille.designation) + " qauntité  " + str(ob.quantity - ob.id_sous_famille.seuil))
    return render(request, "./home/index.html",{"prix":price,"trans":str(nbtrans),"labels":labels,"data":datat,"alert":lt,"list":perd,"stck":requet,"rest":restant,"nbfour":fourni,"Stock":requet,"nbarticle":tot_articl,'tasks':tasks,"allusers":Users,'nb_dem':dem,'nb_rep':rep})

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
         "form":form
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
     
         "form":form
    })

@login_required
def articleUpdate(request,pk):
    artcl = SousFamille.objects.get(id=pk)
    artcl_form = sous_familleForm(instance=artcl)
    if request.method == "POST":
        artcl_form = sous_familleForm(request.POST,instance=artcl)
        if artcl_form.is_valid():
            artcl_form.save()
            return HttpResponseRedirect(reverse("article"))
    return render(request,"./ArticlePage/form.html",{'form':artcl_form})

@login_required
def articledelete(request,pk):
    Sousfamille = SousFamille.objects.get(id=pk)
    if request.method == 'POST':
        Sousfamille.delete()
        return HttpResponseRedirect(reverse("article"))
    return render(request,"/ArticlePage/articles.html",{"artcl":Sousfamille})

@login_required
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
         "form":form
     })     
@login_required
def contrat(request):
     list_contrat=Contrat.objects.all()
     
     return render(request,"./PageContrat/contrat.html",{
         'contrats':list_contrat
        
     }) 
@login_required
def updateContrat(request, pk):
	task = Contrat.objects.get(id=pk)
	form = ContratForm(instance=task)
	if request.method == 'POST':
		form = ContratForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse("Contrat"))
	context = {'form':form}
	return render(request, 'PageContrat/contratForm.html', context)

@login_required
def deleteContrat(request, pk):
	item = Contrat.objects.get(id=pk)
	if request.method == 'POST':
		item.delete()
		return HttpResponseRedirect(reverse("Contrat"))
	context = {'item':item}
	return render(request, 'PageContrat/contrat.html', context)

@login_required
def stock_ajout(request):
      if request.method == 'GET':
        formset = Formsetst(request.GET or None)
        formi = fornisseurform(request.GET or None)
      elif request.method == 'POST':
        formset = Formsetst(request.POST)
        formi = fornisseurform(request.POST)
        if formi.is_valid():
            facutre = Facture.objects.create(phone_number_id=formi.data["phone_number"],ref=formi.data["ref"],Society=formi.data["Society"],dateen=formi.data['dateen'])
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
                
                if(famil.active == 'oui'):
                     Stock(id_sous_famille=famil,quantity=quan,reorder_level=garantie,issue_to = distination,fac=facutre,ci='consommable').save()
                else:
                    for i in range(0,quan):
                        code=str(form.cleaned_data.get('id_sous_famille'))[0:5] + str(famil.id) + str(i)+str(i+1)+str(quan)+str(facutre.id)
                        Stock(id_sous_famille=famil,quantity=1,issue_quantity=0,receive_quantity=0,reorder_level=garantie,fac=facutre,ci=code,issue_to=distination).save()
            facutre.save()
            return HttpResponseRedirect(reverse('stock_details'))
      return render(request,"./PageStock/AjouterStock.html",{"formset":formset,"form":formi})

@login_required
def stock_details(request):
    nb_fac=Stock.objects.values('fac__ref','fac__id','fac__dateen').annotate(Count('quantity')).order_by('fac__dateen')
    tous_article = Stock.objects.all().filter(quantity__gt = 0,issue_to__nom_dis='stock')
    filtrer = ArticleFilter(request.GET,queryset=tous_article)
    s=filtrer.qs.aggregate(Sum('quantity'))['quantity__sum']   
    list_article = filtrer.qs
    return render(request,"./PageStock/stock_delais.html",{'Stock':nb_fac,'filtrer':filtrer,'titre':s})    

@login_required
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
        instance.receive_by=str(request.user)
        instance.issue_to = distinations.objects.get(nom_dis='stock')
        instance.save()
        issue_history = Historique_Stock(
	    last_updated = instance.last_updated,
	    id_sous_famille = instance.id_sous_famille,
	    quantity = instance.quantity, 
	    receive_quantity = instance.receive_quantity, 
	    receive_by = instance.receive_by, 
        issue_to = instance.issue_to,
        ci = instance.id,
        codeibar=instance.ci)
        issue_history.save()
        return HttpResponseRedirect(reverse('stock_details'))
    context = {
			"title": 'Reaceive ' + str(queryset.id_sous_famille),
			"instance": queryset,
			"form": form,
           
			"username": 'Recu a: ' + str(request.user)
            }
	
    return render(request, "./PageStock/receive_form.html", context)

@login_required
def chaque_detail(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"title": queryset.id_sous_famille,
		"queryset": queryset,
	}
	return render(request, "./PageStock/chaque.html", context)

@login_required
def issue_items(request, pk):
    queryset=Stock.objects.get(id=pk)
    form=IssueForm()
    if request.method == 'POST':
        form=IssueForm(request.POST, instance=queryset)
        issue_qt = int(request.POST['issue_quantity'])
    if form.is_valid() and issue_qt <= queryset.quantity:
        try:
            distination = distinations.objects.get(nom_dis="stock")
        except distinations.DoesNotExist:
            distination = distinations(societe='autre',nom_dis="stock")
        instance=form.save(commit=False)
        instance.quantity -= int(request.POST['issue_quantity'])
        instance.issue_quantity = instance.issue_quantity + int(request.POST['issue_quantity'])
        instance.issue_by=str(request.user)
        if queryset.id_sous_famille.active == "oui":
            instance.issue_to=distination
            print('oui')
        else:
            instance.issue_to=instance.issue_to
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
        codeibar=instance.ci
        
        )
        issue_history.save()
        alertquery = Stock.objects.all()
        for alq in alertquery:
            if alq.id_sous_famille.active == "oui" and  alq.quantity < alq.id_sous_famille.seuil:
                email_from = settings.EMAIL_HOST_USER
                try:
                    send_mail("alert stock", "manque de "+ alq.id_sous_famille.designation + "quantite" + str(alq.quantity),email_from,['nasreddine@tanis-tunisie.com'])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.') 
                   
        return HttpResponseRedirect(reverse('stock_details'))

    context = {
			"title": 'Reaceive ' + str(queryset.id_sous_famille),
			"instance": queryset,
			"form": form,
			"username": 'Recu a: ' + str(request.user)
            }
    return render(request, "./PageStock/issue_form.html", context)

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
     
    return render(request,"./PageContrat/contratForm.html",{
        
         "form":form
     }) 

@login_required(redirect_field_name='login')
def Historique(request):
	queryset = Historique_Stock.objects.all()
	context = {
		
		"queryset": queryset,
	}
	return render(request, "./PageStock/historique.html", context)

@login_required(redirect_field_name='login')
def retour_details(request):
    tous_article = Stock.objects.filter(issue_quantity__gt=0)
    filtrer = ArticleFilter(request.GET,queryset=tous_article)
    s=filtrer.qs.aggregate(Sum('quantity'))['quantity__sum']
    list_article = filtrer.qs
    return render(request,"./PageStock/retour_delais.html",{'Stock':list_article,'filtrer':filtrer,'titre':s})   
#########################----------CRUD-Emplacement-----------------------#################
@login_required
def gest_Distinations(request):
    distination = distinations.objects.all()
    context={'emplacement':distination}
    return render(request,"./PageDistination/Distinations.html",context)

@login_required
def add_Distinations(request):
    Dis_Form = DistinationForm()
    if request.method == 'POST':
        Dis_Form = DistinationForm(request.POST)
        if Dis_Form.is_valid():
            Dis_Form.save()
            return HttpResponseRedirect(reverse("gest_Distinations"))
    context={'form':Dis_Form}
    return render(request,"./PageDistination/DistinationForm.html",context)


@login_required
def DistinationUpdate(request,pk):
    emp = distinations.objects.get(id=pk)
    form = DistinationForm(instance=emp)
    if request.method == "POST":
        form = DistinationForm(request.POST,instance=emp)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("gest_Distinations"))
    return render(request,"./PageDistination/DistinationForm.html",{"form":form})

@login_required
def deleteDistination(request,pk):
    emp = distinations.objects.get(id=pk)
    if request.method == 'POST':
        emp.delete()
        return HttpResponseRedirect(reverse("gest_Distinations"))
    return render(request,"./PageDistination/Distinations.html",{"distination":emp})




#########################----------BARCODE-----------------------#################
@login_required
def chaque_Barcode(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"title": queryset.id_sous_famille,
		"queryset": queryset,
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

@login_required
def pdf_view(request, pk):
    template_name = './Pdf_templates/template_facture.html'
    facture_details = Facture.objects.get(id=pk)
    items = Stock.objects.filter(fac__id=pk)
    context = {"ref": facture_details.ref,"societe": facture_details.Society,"date":facture_details.dateen,"fournisseurnom":facture_details.phone_number.nom,"fournisseurmail":facture_details.phone_number.mail,"fac_id": facture_details.id, "items":items}
    return render_to_pdf(template_name,context)

def facture_view(request, pk):
    template_name = './Pdf_templates/viewTemplate.html'
    facture_details = Facture.objects.get(id=pk)
    items = Stock.objects.filter(fac__id=pk)
    context = {"ref": facture_details.ref,"societe": facture_details.Society,"date":facture_details.dateen,"fournisseurnom":facture_details.phone_number.nom,"fournisseurmail":facture_details.phone_number.mail,"fac_id": facture_details.id, "items":items}
    return render(request,template_name,context)

def histbyown(request):     
    data = Historique_Stock.objects.all().values('ci','id_sous_famille__designation','codeibar','id_sous_famille__model').distinct()
    return render(request, "./PageStock/listhistory.html", {"data":data})

def itemhistory(request,pk):     
    infos=Historique_Stock.objects.filter(ci=pk)[0]
    data = Historique_Stock.objects.filter(ci=pk)
    return render(request, "./PageStock/itemhistory.html", {"data":data,"infos":infos})

def item_history_pdf(request,pk): 
    template_name = './Pdf_templates/template_history_item_pdf.html' 
    infos=Historique_Stock.objects.filter(ci=pk)[0]
    data = Historique_Stock.objects.filter(ci=pk)
    context = {"data":data,"infos":infos}
    return render_to_pdf(template_name,context)

#todo goes there===>:

@login_required
def List_tasks(request):
    tasks = Task.objects.filter()
    
    context = {'tasks':tasks, 'form':form}
    return render(request, 'todos/list.html', context)

@login_required
def task_form(request):
    form = TaskForm()
    form.fields['follows'].queryset = User.objects.filter(groups=request.user.groups.all().first())
    if request.method =='POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("list_tasks"))
    context = {'form':form}
    return render(request,'todos/todo_form.html',context)



def List_Voice_tasks(request):
    context={}
    return render(request, 'todos/list_voix.html', context)

def updateTask(request, pk):
	task = Task.objects.get(id=pk)
	form = TaskForm(instance=task)
	if request.method == 'POST':
		form = TaskForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse("list_tasks"))
	context = {'form':form}
	return render(request, 'todos/list.html', context)

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
def Sortie_stock(request):
    tous_article = Stock.objects.all().filter(quantity__gt = 0,issue_to__nom_dis='stock')
    if request.method == 'GET':
        filtrer_gat = request.GET.get('filter_gat')
        if filtrer_gat != '' and filtrer_gat is not None:
            tous_article = tous_article.filter(id_sous_famille__active=filtrer_gat)
    s=tous_article.aggregate(Sum('quantity'))['quantity__sum']
    ms = dumps(s)
    context={'list_article':tous_article,"ms":ms}
    return render(request,"./PageStock/Sortie_Stock.html",context)
def users_view(request):
    users_list = User.objects.values()
    context = {'list_users':users_list}
    return render(request,"./PageUser/users_list.html",context)


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
    return render(request,"./PageUser/users_form.html",{"form":form})
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
    return render(request,"./PageUser/users_form.html",{"form":form})

def deleteUser(request, pk):
	user = User.objects.get(id=pk)
	user.is_active = False
	user.save()
	return HttpResponseRedirect(reverse("users"))
#list_groupe
@login_required(login_url ='/login')
def groups_view(request):
    groups_list = Group.objects.all()
    context = {'list_groups':groups_list}
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
    return render(request,"./PageUser/groups_form.html",{"form":form})

@login_required(login_url ='/login')
def update_group(request,pk):
    group = Group.objects.get(id=pk)
    form = GroupForm(instance=group)
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("groups"))
    return render(request,"./PageUser/groups_form.html",{"form":form})



def listproduct(request):
    list_famille= Familles.objects.all()
    listproduct = Stock.objects.filter(issue_to__nom_dis='stock').values('id_sous_famille__designation','id_sous_famille__designation').annotate(total_qt=Sum('quantity'))
    if request.method == 'POST':
        cat = request.POST['category']
        listproduct = Stock.objects.filter(issue_to__nom_dis='stock',id_sous_famille__id_famille=cat).values('id_sous_famille__designation','id_sous_famille__designation').annotate(total_qt=Sum('quantity'))
    context = {'listProducts':listproduct,'list_famille':list_famille}
    return render(request,"./demandes/list_demandes.html",context)

def listdemandes(request):
    listdemande = demande.objects.all()
    context = {'listdemandes':listdemande}
    return render(request,"./demandes/verification_demande.html",context)

def verifier_demandes(request,pk):
    demand = demande.objects.get(id=pk)
    if request.method == "POST":
        verif= request.POST['verifier']
        if verif == "livrer":
            demand.validation=verif
            email_from = settings.EMAIL_HOST_USER
            user_group = demand.demander.groups.all().first()
            print(user_group)
            group=Group.objects.get(id=user_group.id)
            email_to=group.email
            print(email_to)
            demand.save()
            try:
                send_mail("demande materiel", " demande de "+str(demand.article.id_sous_famille.designation)+" valider Par "+str(request.user),email_from,[email_to])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        else:
            demand.validation=verif
            demand.save()   
    return HttpResponseRedirect(reverse('list_demande'))

def demande_product(request,pk):
    article = Stock.objects.filter(id_sous_famille__designation=pk)
    getarticle = Stock.objects.get(id=article[0].id)
    if request.method == "POST":
        quantite = request.POST[pk]
        if quantite:
            demande.objects.create(article = article[0],demander = request.user,quantite = quantite)
            email_from = settings.EMAIL_HOST_USER
            email_to = str(getarticle.id_sous_famille.groupresp.email)
            print(email_to)
            try:
                send_mail("demande materiel", "Par "+str(request.user)+" demande de "+str(getarticle.id_sous_famille.designation)+"  quantiter: "+str(quantite),email_from,[email_to])
            except BadHeaderError:
                return HttpResponse('Invalid header found.') 
    return HttpResponseRedirect(reverse("list_product"))
    
@login_required
def list_reparated(request):
    list_rep = Stock.objects.all()
    em=['case','stock','reparation']
    for e in em:
        list_rep = list_rep.filter(~Q(issue_to__nom_dis=e))
    context={'list_rep':list_rep}
    return render(request,"./demandes/demande_reparation.html",context)


@login_required
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
    context={'item':item}
    return render(request,"./demandes/reparation_form.html",context)

@login_required
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
    context={'list_recla':list_reclamation,'titre_etat':mot_etat}
    return render(request,"./demandes/list_reparation.html",context)

@login_required
def verfication_reparation(request,pk):
    reclamation = reparation_materiel.objects.get(id = pk)
    if request.method == 'POST':
        etat = request.POST['etat']
        reclamation.etat = etat
        reclamation.save()
        if etat == 'case':
            emplacement,created = distinations.objects.get_or_create(nom_dis='case')
            item = Stock.objects.get(id=reclamation.article.id)
            item.issue_to=emplacement
            item.save()
            issue_history = Historique_Stock(
	        last_updated = item.last_updated,
	        id_sous_famille = item.id_sous_famille,
	        quantity = item.quantity, 
	        receive_quantity = item.receive_quantity, 
	        receive_by = item.receive_by, 
            issue_to = item.issue_to,
            ci = item.id,
            codeibar=item.ci)
            issue_history.save()
        elif etat =='en-cours':
            emplacement,created = distinations.objects.get_or_create(nom_dis='reparation')
            item = Stock.objects.get(id=reclamation.article.id)
            item.issue_to=emplacement
            item.save()
            issue_history = Historique_Stock(
	        last_updated = item.last_updated,
	        id_sous_famille = item.id_sous_famille,
	        quantity = item.quantity, 
	        receive_quantity = item.receive_quantity, 
	        receive_by = item.receive_by, 
            issue_to = item.issue_to,
            ci = item.id,
            codeibar=item.ci)
            issue_history.save()
        elif etat == "resolu":
            item = Stock.objects.get(id=reclamation.article.id)
            if item.issue_to.nom_dis != 'reparation':
                item.save()
            else:
                last_em=Historique_Stock.objects.filter(codeibar=item.ci).order_by('last_updated')
                if len(last_em)<=1:
                    sl=len(last_em)-1
                else:
                    sl= len(last_em)-2
                empt=last_em[sl].issue_to
                emp=distinations.objects.get(nom_dis=empt)
                item.issue_to=emp
                item.save()
        return HttpResponseRedirect(reverse('list_reclamation'))

    context={"reclamation":reclamation}
    return render(request,"./demandes/verification_reparation.html",context)
@login_required
def emplacement_societe(request):
    items = Stock.objects.filter(issue_quantity__gt=0)
    distination = distinations.objects.all()
    reclamation=reparation_materiel.objects.filter(etat='en-cours')
    nb_dis=distinations.objects.values('societe').annotate(Count('societe')).order_by().filter(societe__count__gte=1)
    context = {'items':items,'distinations':distination,'soc_prod':nb_dis,'rec':reclamation}
    return render(request,"./PageDistination/societe_emplacement.html",context)

@login_required
def items_Distinations(request,pk):
    items = Stock.objects.filter(issue_quantity__gt=0,issue_to__societe=pk,id_sous_famille__active='non')
    distination = distinations.objects.filter(societe=pk)
    reclamation=reparation_materiel.objects.filter(etat='en-cours')
    context = {'items':items,'distinations':distination,'rec_item':reclamation}
    return render(request,"./PageDistination/item_emplacement.html",context)

@login_required
def box_details(request,pk):
    items = Stock.objects.filter(issue_quantity__gt=0,issue_to__id=pk,id_sous_famille__active='non')
    distination = distinations.objects.get(id=pk)
    reclamation=reparation_materiel.objects.filter(etat='en-cours')
    context = {'items':items,'distination':distination,'rec':reclamation}
    return render(request,"./PageDistination/box_details.html",context)

@login_required
def emplacement_autre(request):
    items = Stock.objects.filter(issue_quantity__gt=0)
    distination = distinations.objects.all()
    reclamation=reparation_materiel.objects.all()
    nb_dis=distinations.objects.values('societe').annotate(Count('societe')).order_by().filter(societe__count__gte=1)
    context = {'items':items,'distinations':distination,'soc_prod':nb_dis,'rec':reclamation}
    return render(request,"./PageDistination/autre_emplacement.html",context)
