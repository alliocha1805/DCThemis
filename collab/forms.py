from django import forms
from django.contrib.staticfiles.utils import get_files
from django.contrib.staticfiles.storage import StaticFilesStorage

class CvTemplateForm(forms.Form):
    s = StaticFilesStorage()
    repertoire=[]
    repertoire_pas_propre=list(get_files(s, location='collab'))
    for elt in repertoire_pas_propre:
        if "assets" in elt:
            pass
        else:
            nomDoc = elt.replace("collab\\",'')
            if ".docx" in nomDoc:
                valeur=(nomDoc,nomDoc)
                repertoire.append(valeur)
            else:
                pass
    template = forms.CharField(label='Quel template voulez-vous ?', widget=forms.Select(choices=repertoire))
    collabid=forms.CharField(widget = forms.HiddenInput(), required = True)