from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader, Context
from django.views.generic import CreateView
from collab.models import competences,client,collaborateurs,outils,experiences, projet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from operator import itemgetter
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import datetime
import locale
from xhtml2pdf import pisa 
import bs4
from docxtpl import DocxTemplate, RichText, Listing
import io
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.finders import find
import os
from django.conf import settings
from django.contrib.staticfiles.utils import get_files
from django.contrib.staticfiles.storage import StaticFilesStorage
from .forms import CvTemplateForm
#Calcul du nb de consultant actif
def nbConsultantActif():
    compteur=0
    consultants=collaborateurs.objects.all()
    for elt in consultants:
        dateDepart=elt.dateSortie
        if not dateDepart:
            compteur+=1
        elif dateDepart > datetime.date.today():
            compteur+=1
        else:
            pass
    return compteur
# Homepage
def index(request):
    template = loader.get_template('collab/index2.html')
    nbConsultant = nbConsultantActif()
    nbConsultantInterco = collaborateurs.objects.filter(estEnIntercontrat=True).count()
    nbConsultantEnMission = nbConsultant - nbConsultantInterco
    txInterco = round((nbConsultantInterco / nbConsultantActif())*100,1)
    nbCompe = competences.objects.count()
    nbOutils = outils.objects.count()
    nbClient = client.objects.count()
    #Verification qu'un projet est actif (donc avec au moins une mission en cours)
    def verifProjetActif(idProjet):
        projetaTest = projet.objects.filter(pk=idProjet)
        if not projetaTest:
            statut = "PAS ACTIF"
        else:
            expesATest = experiences.objects.filter(projetDeLaMission=projetaTest[0].pk)
            if not expesATest:
                statut = "PAS ACTIF"
            else:
                for elt in expesATest:
                    dateDeFin = elt.dateFin
                    if dateDeFin == None:
                        statut = "ACTIF"
                        break
                    elif dateDeFin > datetime.date.today(): 
                        statut = "ACTIF"
                        break
                    else:
                        statut = "PAS ACTIF"
        return statut
    def VerifMissionEnCours(idMission):
        missionaTest=get_object_or_404(experiences, pk=idMission)
        today = datetime.date.today()
        dateFinMission = missionaTest.dateFin
        if not dateFinMission:
            statut = "ACTIF"
        elif dateFinMission < today:
            statut = "ACTIF"
        else:
            statut = "INACTIF"
        return statut
    #calcul du nombre de client actif (a savoir les clients avec une mission en cours a date) A REWORK car expe n'ont plus de client
    def getClientActif():
        client_total=client.objects.all()
        count=0
        for elt in client_total:
            missions = experiences.objects.filter(client=elt.id)
            if not missions:
                pass
            else:
                for miss in missions:
                    statut = VerifMissionEnCours(miss.pk)
                    if statut == "ACTIF":
                        count+=1
                        break
                    else:
                        continue
        return(count)
    nbClientActif = getClientActif()
    nbClientInactif = nbClient - nbClientActif
    txClientInactif = round((nbClientInactif / nbClient)*100,1)
    #calcul du nombre de competence moyen par consultant
    def getMoyenneCompetence():
        listeCompe=[]
        listeCollab=collaborateurs.objects.all()
        for elt in listeCollab:
            nb_compe_calcul = elt.listeCompetencesCles.count()
            listeCompe.append(nb_compe_calcul)
        moyenne=(sum(listeCompe)/len(listeCompe))
        return(moyenne)
    def getMoyenneOutil():
        listeOutil=[]
        listeCollab=collaborateurs.objects.all()
        for elt in listeCollab:
            nb_outil_calcul = elt.outilsCollaborateur.count()
            listeOutil.append(nb_outil_calcul)
        moyenne=(sum(listeOutil)/len(listeOutil))
        return(moyenne)
    moyenneOutil = round(getMoyenneOutil(),1)
    moyenneCompetence = round(getMoyenneCompetence(),1)
    #calcul top 5 des outils - la fonction retourne l'outil en position N du top
    def getTop5Outils():
        listeCollab=collaborateurs.objects.all()
        dicoOutil_temp={}
        #on récupère les outils de chaque collab et on fait un dictionnaire sous la forme {"outil1":"nb de consultant l'ayant)"}
        for collab in listeCollab:
            liste_outil_collab = collab.outilsCollaborateur.values()
            for elt in liste_outil_collab:
                outil = elt['nomOutil']
                if outil in dicoOutil_temp:
                    nb_temp = dicoOutil_temp.get(outil)
                    dicoOutil_temp[outil]=nb_temp+1
                else:
                    dicoOutil_temp[outil]=1
        #on trie le dictionnaire par valeur
        dicoOutil = sorted(dicoOutil_temp.items(), key=lambda x: x[1], reverse=True)
        #on récupère les valeurs en iterant sur le nouveau dictionnaire et on met dans une liste
        topOutil=[x[0] for x in dicoOutil]
        topfinal=topOutil[:5]
        return topfinal
    topOutilfront = getTop5Outils()    

    #calcul top 5 des competences - la fonction retourne la competence en position N du top
    def getTop5Competences():
        listeCollab=collaborateurs.objects.all()
        dicoCompetences_temp={}
        #on récupère les competences de chaque collab et on fait un dictionnaire sous la forme {"competence1":"nb de consultant l'ayant)"}
        for collab in listeCollab:
            liste_compe_collab = collab.listeCompetencesCles.values()
            for elt in liste_compe_collab:
                competence = elt['nomCompetence']
                if competence in dicoCompetences_temp:
                    nb_temp = dicoCompetences_temp.get(competence)
                    dicoCompetences_temp[competence]=nb_temp+1
                else:
                    dicoCompetences_temp[competence]=1
        #on trie le dictionnaire par valeur
        dicoCompetences = sorted(dicoCompetences_temp.items(), key=lambda x: x[1], reverse=True)
        #on récupère les valeurs en iterant sur le nouveau dictionnaire et on met dans une liste
        topCompetence=[x[0] for x in dicoCompetences]
        topfinal=topCompetence[:5]
        return topfinal
    topCompetencefront = getTop5Competences()   
    context={
    "nbConsultant":nbConsultant,
    "nbConsultantInterco":nbConsultantInterco,
    "txInterco":txInterco,
    "nbConsultantEnMission":nbConsultantEnMission,
    "nbClient":nbClient,
    "nbClientActif":nbClientActif,
    "nbClientInactif":nbClientInactif,
    "txClientInactif":txClientInactif,
    "nbCompe":nbCompe,
    "moyenneCompetence":moyenneCompetence,
    'topCompetencefront':topCompetencefront,
    'nbOutils':nbOutils,
    'moyenneOutil':moyenneOutil,
    'topOutilfront':topOutilfront
    }
    return HttpResponse(template.render(context, request))

# Liste consultant PAGINEE
def liste_consultant(request):
    template = loader.get_template('collab/liste_consultant_recherche.html')
    collab_list= collaborateurs.objects.all().order_by('nomCollaborateur')
    context={'collabs':collab_list}
    return HttpResponse(template.render(context, request))

# Liste consultant ACTifs
def liste_consultant_actif(request):
    template = loader.get_template('collab/liste_consultant_recherche.html')
    collab_list= collaborateurs.objects.all().order_by('nomCollaborateur')
    collabs=[]
    for coll in collab_list:
        dateDepart=coll.dateSortie
        if not dateDepart:
            collabs.append(coll)
        elif dateDepart > datetime.date.today():
            collabs.append(coll)
        else:
            continue
    context={'collabs':collabs}
    return HttpResponse(template.render(context, request))

# Liste consultant ACTifs et en mission
def liste_consultant_actif_et_en_mission(request):
    template = loader.get_template('collab/liste_consultant_recherche.html')
    collab_list= collaborateurs.objects.all().order_by('nomCollaborateur')
    collabs=[]
    collabs_mission=[]
    for coll in collab_list:
        dateDepart=coll.dateSortie
        if not dateDepart:
            collabs.append(coll)
        elif dateDepart > datetime.date.today():
            collabs.append(coll)
        else:
            continue
    for elt in collabs:
        missionsCollab=experiences.objects.filter(collaborateurMission=elt.pk)
        if not missionsCollab:
            continue
        else:
            for miss in missionsCollab:
                dateFinMiss=miss.dateFin
                if not dateFinMiss:
                    collabs_mission.append(elt)
                    break
                elif dateFinMiss > datetime.date.today():
                    collabs_mission.append(elt)
                    break
                else:
                    continue
    context={'collabs':collabs_mission}
    return HttpResponse(template.render(context, request))

# Liste consultant en interco
def liste_consultant_interco(request):
    template = loader.get_template('collab/liste_consultant_recherche.html')
    collab_list= collaborateurs.objects.filter(estEnIntercontrat=True).order_by('nomCollaborateur')
    context={'collabs':collab_list}
    return HttpResponse(template.render(context, request))

#Detail consultant
def collaborateur_detail(request, collaborateurs_id):
    collab = get_object_or_404(collaborateurs, pk=collaborateurs_id)
    mission_du_collab = experiences.objects.filter(collaborateurMission=collaborateurs_id).order_by('-dateDebut')
    expeSingificatives=[]
    expeSingificatives.append(collab.expSignificative1)
    expeSingificatives.append(collab.expSignificative2)
    expeSingificatives.append(collab.expSignificative3)
    expeSingificatives.append(collab.expSignificative4)
    expeSingificatives.append(collab.expSignificative5)
    formations=[]
    for form in collab.formation.all().order_by('formation__obtentionformation__dateObtention'):
        annee=form.get_year()
        diplome=form.formation.diplome
        ecole=form.formation.ecole
        formations.append(str(annee)+" - "+diplome+" - "+ecole)
    template = loader.get_template('collab/detail_consultant2.html')
    context={'collab':collab, 'mission_du_collab':mission_du_collab,'expeSingificatives':expeSingificatives,'formations':formations}
    return HttpResponse(template.render(context, request))
#Ajout d'un consultant
class collaborateursCreateView(CreateView):
    model = collaborateurs
    fields = ('nomCollaborateur', 'prenomCollaborateur','trigramme','titreCollaborateur','dateDeNaissance','texteIntroductifCv','dateDebutExpPro','codePostal','telephone','listeCompetencesCles','formation','parcours','methodologie','langues','outilsCollaborateur','estEnIntercontrat')
    success_url = 'succes/'
def reussite_ajout_collaborateurs(request):
    template = loader.get_template('collab/reussite_ajout_collaborateurs2.html')
    context={}
    return HttpResponse(template.render(context, request))

#Liste client PAGINEE
def liste_client(request):
    template = loader.get_template('collab/liste_client2.html')
    client_list= client.objects.all().order_by('nomClient')
    context={'clients':client_list}
    return HttpResponse(template.render(context, request))
#Fonction de verification de mission en cours
def VerifMissionEnCours(idMission):
    missionaTest=get_object_or_404(experiences, pk=idMission)
    today = datetime.date.today()
    dateFinMission = missionaTest.dateFin
    if not dateFinMission:
        statut = "ACTIF"
    elif dateFinMission < today:
        statut = "ACTIF"
    else:
        statut = "INACTIF"
    return statut
#Liste client actif
def liste_client_actif(request):
    template = loader.get_template('collab/liste_client2.html')
    client_list= client.objects.all()
    clients=[]
    for elt in client_list:
        missionsDuClient = experiences.objects.filter(client=elt.id)
        for mission in missionsDuClient:
            statut = VerifMissionEnCours(mission.pk)
            if statut == "ACTIF":
                clients.append(elt)
                break
            else:
                continue
    context={'clients':clients}
    return HttpResponse(template.render(context, request))
#Liste client inactif
def liste_client_inactif(request):
    template = loader.get_template('collab/liste_client2.html')
    client_list= client.objects.all()
    clients_actif=[]
    for elt in client_list:
        missionsDuClient = experiences.objects.filter(client=elt.id)
        for mission in missionsDuClient:
            statut = VerifMissionEnCours(mission.pk)
            if statut == "ACTIF":
                clients_actif.append(elt)
                break
            else:
                continue
    clients = list(set(client_list) - set(clients_actif))
    context={'clients':clients}
    return HttpResponse(template.render(context, request))
#Ajout d'un client
class clientCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = client
    fields = ('nomClient', 'domaineClient','logoClient')
    success_url = 'succes/'
def reussite_ajout_client(request):
    template = loader.get_template('collab/reussite_ajout_client2.html')
    context={}
    return HttpResponse(template.render(context, request))  

# Liste consultant Par Client
def liste_consultant_client(request,client_id):
    template = loader.get_template('collab/liste_consultant_recherche.html')
    expe_list= experiences.objects.filter(client=client_id)
    collab_list=[]
    for elt in expe_list:
        collab_id=elt.collaborateurMission.pk
        collab=get_object_or_404(collaborateurs, pk=collab_id)
        collab_list.append(collab)
    context={'collabs':collab_list}
    return HttpResponse(template.render(context, request))

#Liste compétences PAGINEE EN FRONT
def liste_competence(request):
    template = loader.get_template('collab/liste_competence2.html')
    compe_list= competences.objects.all().order_by('famille')
    context={'compes':compe_list}
    return HttpResponse(template.render(context, request))
#Ajout d'une competence
class competencesCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = competences
    fields = ('nomCompetence', 'famille')
    success_url = 'succes/'

def reussite_ajout_competence(request):
    template = loader.get_template('collab/reussite_ajout_compe2.html')
    context={}
    return HttpResponse(template.render(context, request))
# Liste consultant Par compétence
def liste_consultant_competence(request,competences_id):
    template = loader.get_template('collab/liste_consultant_recherche.html')
    collab_list= collaborateurs.objects.filter(listeCompetencesCles=competences_id)
    context={'collabs':collab_list}
    return HttpResponse(template.render(context, request))

#Liste outil REELLEMENT PAGINEE
def liste_outil(request):
    template = loader.get_template('collab/liste_outil2.html')
    outils_list= outils.objects.all().order_by('famille')
    page = request.GET.get('page', 1)
    paginator = Paginator(outils_list, 100)
    try:
        tools= paginator.page(page)
    except PageNotAnInteger:
        tools = paginator.page(1)
    except EmptyPage:
        tools = paginator.page(paginator.num_pages)
    context={'tools':tools}
    return HttpResponse(template.render(context, request))

def liste_outil_propre(request):
    template = loader.get_template('collab/liste_outil2.html')
    outils_list= outils.objects.all().order_by('famille')
    context={'tools':outils_list}
    return HttpResponse(template.render(context, request))

class outilsCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = outils
    fields = ('nomOutil', 'famille')
    success_url = 'succes/'
def reussite_ajout_outil(request):
    template = loader.get_template('collab/reussite_ajout_outil2.html')
    context={}
    return HttpResponse(template.render(context, request))
# Liste consultant Par Outil
def liste_consultant_outil(request,outil_id):
    template = loader.get_template('collab/liste_consultant_recherche.html')
    collab_list= collaborateurs.objects.filter(outilsCollaborateur=outil_id)
    context={'collabs':collab_list}
    return HttpResponse(template.render(context, request))

#Page CV
def page_cv_html(request, collaborateurs_id):
    collab = get_object_or_404(collaborateurs, pk=collaborateurs_id)
    mission_du_collab = experiences.objects.filter(collaborateurMission=collaborateurs_id).order_by('-dateDebut')
    template = loader.get_template('collab/CV_TEST.html')
    context={'collab':collab, 'mission_du_collab':mission_du_collab}
    return HttpResponse(template.render(context, request))

#Page CV en pdf
def page_cv_pdf(request, collaborateurs_id):
    collab = get_object_or_404(collaborateurs, pk=collaborateurs_id)
    mission_du_collab = experiences.objects.filter(collaborateurMission=collaborateurs_id).order_by('-dateDebut')
    template = loader.get_template('collab/CV_TEST.html')
    context={'collab':collab, 'mission_du_collab':mission_du_collab}
    html = template.render(context, request)
    file = open('test.pdf', "w+b")
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
    file.seek(0)
    pdf = file.read()
    file.close()
    return HttpResponse(pdf, 'application/pdf')

# Fonction de parsing du HTML pour la generation de CV
def make_tree(body: bs4.Tag):
    branch = []
    for ch in body.children:
        if isinstance(ch, bs4.NavigableString):
            if str(ch).strip():
                branch.append(str(ch).strip())
        else:
            branch.append(make_tree(ch))
    return branch


def decoupe_html (raw_html):
    soup=bs4.BeautifulSoup(raw_html,"html.parser")
    arbre=[]
    #decoupe en grand bloc HTML
    for elt in soup:
        arbre.append(elt)
    #On parcours chaque elt pour le transformer en truc compréhensible par Word dans une liste
    for elt in arbre:
        #recup du tag de début du "chunk"
        tag=elt.name
        #traitement des paragraphe de texte
        if tag == "p":
            texte=elt.text
            place=arbre.index(elt)
            arbre[place]=texte
        #traitement des listes
        elif tag == "ul":
            soup = bs4.BeautifulSoup(str(elt), 'html.parser')
            tree = make_tree(soup.select_one('ul'))
            place=arbre.index(elt)
            arbre[place]=tree
    return(arbre)
def DC_RT_Texte (rt, soup_text, dc_style):
    try:
        rt.add_paragraph(soup_text, style=dc_style)
    except:
        print ("PROBLEME : rt.add_paragraph('"+soup_text.string+"\a', style='"+dc_style+"')")
    return rt
def DC_RT_P (rt, soup_text, dc_style):
    for soup_element in soup_text.contents:
        rt = DC_RT_Texte(rt, soup_element.string, dc_style+"_Paragraphe")
    return rt
def DC_RT_LI (rt, soup_text, dc_style, dc_level):
    for soup_element in soup_text.contents:
        if isinstance(soup_element, str):
            rt = DC_RT_Texte(rt, soup_element.string, dc_style+"_Puce"+str(dc_level))
        elif soup_element.name =="ul":
            rt = DC_RT_UL (rt, soup_element, dc_style, dc_level+1)
    return rt
def DC_RT_UL (rt, soup_text, dc_style, dc_level):
    for soup_element in soup_text.contents:
        if isinstance(soup_element, str):
            #on fait rien
            do_nothing=1
        elif soup_element.name == "li":
            rt = DC_RT_LI (rt, soup_element, dc_style, dc_level)
    return rt
def generateRichText (doc, html_text, dc_style):
    rt = doc.new_subdoc()
    IsHtmlElement = bool(bs4.BeautifulSoup(html_text, "html.parser").find())
    if bool(bs4.BeautifulSoup(html_text, "html.parser").find()):
        html_text = html_text.replace('\n','')
        html_text = html_text.replace('\r','')
        html_text = html_text.replace('\t','')
        soup_text = bs4.BeautifulSoup(html_text, "html.parser")
        for soup_element in soup_text.contents:
            if isinstance(soup_element, str):
                #on fait rien
                do_nothing=1
            elif soup_element.name == "p":
                rt = DC_RT_P (rt, soup_element, dc_style)
            elif soup_element.name == "ul":
                rt = DC_RT_UL (rt, soup_element, dc_style, 1)
    else:
        rt = DC_RT_Texte(rt, html_text, dc_style)
    return rt
def generateRichText2(doc, raw_html, DC_STYLE):
    listePropre = decoupe_html (raw_html)
    rt = RichText(style=DC_STYLE)
    for elt in listePropre:
        #Gestion des paragraphes
        if type(elt) == type('une string'):
            if listePropre.index(elt) == 0:
                rt.add(elt+'\n')
            else:
                text='\a'+elt+'\n'
                rt.add(text)
        #Gestion des listes
        elif type(elt) == list:
            ul=elt
            #parcours des elements de la liste ul
            for elt in ul:
                for li in elt:
                    #niv 1
                    if type(li) == type('une string'):
                        rt.add("• "+li+"\n")
                    #sinon
                    elif type(li) == list:
                        for subul in li:
                            for subli in subul:
                                #niv 2
                                if type(subli) == type('une string'):
                                    rt.add("\t"+"○ "+subli+"\n")
                                #sinon
                                elif type(subli) == list:
                                    for subsubul in subli:
                                        for subsubli in subsubul:
                                            #niv 3
                                            if type(subsubli) == type('une string'):
                                                rt.add("\t\t"+"◙ "+subsubli+"\n")
                                            #sinon
                                            elif type(subsubli) == list:
                                                for subsubsubul in subsubli:
                                                    for subsubsubli in subsubsubul:
                                                        #niv4
                                                        if type(subsubsubli) == type('une string'):
                                                            rt.add("\t\t\t"+"■ "+subsubsubli+"\n")
                                                
    return(rt)
#Page CV docx
def page_cv_word_choix_template(request, collaborateurs_id, template_path):
    collab = get_object_or_404(collaborateurs, pk=collaborateurs_id)
    mission_du_collab = experiences.objects.filter(collaborateurMission=collaborateurs_id).order_by('-dateDebut')
    fichier_template = staticfiles_storage.path(template_path)
    doc = DocxTemplate(fichier_template)
    today = datetime.date.today()
    context = {}
    nom = collab.nomCollaborateur
    prenom = collab.prenomCollaborateur
    nom_sortie = nom + "-"+prenom+"-"+str(today)+".docx"
    titre = collab.titreCollaborateur
    #calcul nb année expe
    if isinstance(collab.dateDebutExpPro,datetime.date):
        dateExpeDebutAnne = collab.dateDebutExpPro.year
    else:
        dateExpeDebutAnne = datetime.date.today().year	
    anneeActuelle = datetime.date.today().year
    differenceExpe = anneeActuelle - dateExpeDebutAnne
    nbAnneeExpe = differenceExpe
    texte_introductif = generateRichText(doc, collab.texteIntroductifCv, "DC_Text_Intro")
    #recup des compétences
    competencesDuCollab = collab.listeCompetencesCles.all()
    competences=[]
    for compe in competencesDuCollab:
        competences.append(compe.nomCompetence)
    #recup des niveau d'intervention
    NivInterven = collab.niveauxIntervention.all()
    interventions=[]
    for inter in NivInterven:
        interventions.append(inter.libelle)
    #recup des clients principaux
    clientsPrincipaux = collab.clientPrincipaux.all()
    clients=[]
    for client in clientsPrincipaux:
        clients.append(client.nomClient)
    #recup des secteur
    SecteurConsult = collab.expertiseSectorielle.all()
    secteurs=[]
    for secteur in SecteurConsult:
        secteurs.append(secteur.nom)
    #recup des outils ANCIENNE FONCTION
    OutilsConsult = collab.outilsCollaborateur.all()
    outils=[]
    #on groupe les résultat dans un dictionnaire {famille:[outil1,outil2],famille2:[outil1,outil2]}
    groupementOutil={}
    for outil in OutilsConsult:
        famille=outil.famille
        nom=outil.nomOutil
        #on verifie si la famille outil est deja dans le dictionnaire
        if famille in groupementOutil:
            #on ajoute la valeur a la liste d'outils
            liste=groupementOutil.get(famille)
            liste= liste + ", " + nom
            groupementOutil[famille]=liste
        else:
            groupementOutil[famille]=nom
    for key in groupementOutil:
        outils.append(str(key)+" : "+groupementOutil.get(key))
    #Nouvelle fonction Outil par Olivier le 21/07/2020
    groupementOutil2={}
    for outil in OutilsConsult:
        famille=outil.famille
        nom=outil.nomOutil
        #on verifie si la famille outil est deja dans le dictionnaire
        if famille not in groupementOutil2:
            groupementOutil2[famille]=[]
        groupementOutil2[famille].append(nom)
    outils2=[]
    for famillesO in groupementOutil2:
        data={}
        data["famille"]=famillesO
        data["outils"]=[]
        for outilO in groupementOutil2[famillesO]:
            data["outils"].append(outilO)
        outils2.append(data)
    context["outils2"]=outils2
    #recup des langues
    LanguesConsult = collab.langues.all()
    langues=[]
    for langue in LanguesConsult:
        langues.append(langue)
    #recup des methodlogies
    MethodoConsult = collab.methodologie.all()
    methodologies=[]
    for methodo in MethodoConsult:
        methodologies.append(methodo.nom)
    #recup des formations simple
    FormationConsult = collab.formation.all().order_by('formation__obtentionformation__dateObtention')
    formations=[]
    for forma in FormationConsult:
        annee=forma.get_year()
        diplome=forma.formation.diplome
        ecole=forma.formation.ecole
        formations.append(str(annee)+" : "+diplome+" - "+ecole)
    #Formation en double boucle
    formations2=[]
    for forma in FormationConsult:
        data={}
        data["annee"]=forma.get_year()
        data["diplome"]=forma.formation.diplome
        data["ecole"]=forma.formation.ecole
        data["formation"]=(str(data["annee"])+" : "+data["diplome"]+" - "+data["ecole"])
        formations2.append(data)
    context["formations2"]=sorted(formations2, key=lambda col: col["annee"])
    context["formations2_desc"]=sorted(formations2, key=lambda col: col["annee"], reverse=True)
    #recup des expe significatives
    expeSignificatives=[]
    if collab.expSignificative1:
        expeSignificatives.append(collab.expSignificative1)
    else:
        pass
    if collab.expSignificative2:
        expeSignificatives.append(collab.expSignificative2)
    else:
        pass
    if collab.expSignificative3:
        expeSignificatives.append(collab.expSignificative3)
    else:
        pass
    if collab.expSignificative4:
        expeSignificatives.append(collab.expSignificative4)
    else:
        pass
    if collab.expSignificative5:
        expeSignificatives.append(collab.expSignificative5)
    else:
        pass
    #recup des missions (il faut tout recup car impossible d'utiliser les templatetags avec du Word)
    missions=[]
    locale.setlocale(locale.LC_ALL, 'fr_FR')
    for miss in mission_du_collab:
        data={}
        data["nomMission"]=miss.nomMission
        data["Client"]=miss.client.nomClient
        data["Domaine"]=miss.client.domaineClient
        data["Service"]=miss.service
        data["dateDebut"]=miss.dateDebut
        data["dateDebut_mmmm_aaaa"]=miss.dateDebut.strftime("%B %Y")
        data["dateDebut_mmm-aaaa"]=miss.dateDebut.strftime("%b-%Y")
        data["dateDebut_aaaa"]=miss.dateDebut.strftime("%Y")
        #calcul durée
        dateFin=miss.dateFin
        if dateFin is None:
            fin = datetime.date.today()
            debut = miss.dateDebut
            dureeMission = (fin.year - debut.year) * 12 + (fin.month - debut.month)+ 1
            data["dateFin"]="Aujourd'hui"
            data["dateFin_mmmm_aaaa"]="Aujourd'hui"
            data["dateFin_mmm-aaaa"]="Aujourd'hui"
            data["dateFin_aaaa"]="Aujourd'hui"
        else:
            fin = miss.dateFin
            debut = miss.dateDebut
            dureeMission = (fin.year - debut.year) * 12 + (fin.month - debut.month) + 1
            data["dateFin"]=miss.dateFin
            data["dateFin_mmmm_aaaa"]=miss.dateFin.strftime("%B %Y")
            data["dateFin_mmm-aaaa"]=miss.dateFin.strftime("%b-%Y")
            data["dateFin_aaaa"]=miss.dateFin.strftime("%Y")
        data["dureeMission"]=dureeMission
        data["contexteMission"]=generateRichText(doc,miss.resumeIntervention, "DC_Intervention_Contexte")
        data["descriptif"]=generateRichText(doc, miss.descriptifMission, "DC_Intervention_Desc")
        data["environnement"]=generateRichText(doc, miss.environnementMission, "DC_Intervention_Env")
        missions.append(data)

    #Ajout des valeurs dans le context          
    context["nom"]=nom
    context["prenom"]=prenom
    context["titre"]=titre
    context["grade"]=collab.get_grade_display()
    context["trigramme"]=collab.trigramme
    context["nbAnneeExpe"]=nbAnneeExpe
    context["text_intro"]=texte_introductif
    context["expeSignificatives"]=expeSignificatives
    context["competences"]=competences
    context["Interventions"]=interventions
    context["clients"]=clients
    context["secteurs"]=secteurs
    context["outils"]=outils
    context["langues"]=langues
    context["methodologies"]=methodologies
    context["formations"]=formations
    context["missions"]=missions
    context["parcours"]=generateRichText(doc,collab.parcours, "DC_Parcours")
    doc.render(context)
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    response = HttpResponse(doc_io.read())
    response["Content-Disposition"] = "attachment; filename="+nom_sortie
    response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    return response


#Vue form choix template CV
def recup_option_cv(request, collaborateurs_id):
    if request.method == 'POST':
        form = CvTemplateForm(request.POST)
        if form.is_valid():
           template = form.cleaned_data['template']
           template_path='collab\\'+template
           return page_cv_word_choix_template(request, collaborateurs_id,template_path)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = CvTemplateForm()
        form.initial['collabid'] = collaborateurs_id

    return render(request, 'collab/choix_option_cv.html', {'form': form})
#Page liste intervention
def liste_intervention(request):
    template = loader.get_template('collab/liste_intervention.html')
    mission_list= experiences.objects.all().order_by('nomMission')
    context={'missions':mission_list}
    return HttpResponse(template.render(context, request))