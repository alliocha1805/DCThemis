from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('consultant/', views.liste_consultant, name='liste_consultant'),
    path('consultant/compe/<int:competences_id>/', views.liste_consultant_competence, name='liste_consultant_competence'),
    path('consultant/outil/<int:outil_id>/', views.liste_consultant_outil, name='liste_consultant_outil'),
    path('consultant/client/<int:client_id>/', views.liste_consultant_client, name='liste_consultant_client'),
    path('consultant/<int:collaborateurs_id>/', views.collaborateur_detail, name='collaborateur_detail'),
    path('consultant/<int:collaborateurs_id>/cv_html', views.page_cv_html, name='page_cv_html'),
    path('consultant/<int:collaborateurs_id>/cv_html/pdf', views.page_cv_pdf, name='page_cv_pdf'),
    path('consultant/<int:collaborateurs_id>/cv_word', views.page_cv_word_choix_template, name='page_cv_word_choix_template'),
    path('consultant/<int:collaborateurs_id>/cv_word/option', views.recup_option_cv, name='recup_option_cv'),
    path('consultant/ajout/', views.collaborateursCreateView.as_view(), name='collaborateursCreateView'),
    path('consultant/ajout/succes/', views.reussite_ajout_collaborateurs, name='reussite_ajout_collaborateurs'),
    path('client/', views.liste_client, name='liste_client'),
    path('client/actif/', views.liste_client_actif, name='liste_client_actif'),
    path('client/inactif/', views.liste_client_inactif, name='liste_client_inactif'),
    path('client/ajout/', views.clientCreateView.as_view(), name='clientCreateView'),
    path('client/ajout/succes/', views.reussite_ajout_client, name='reussite_ajout_client'),
    path('competence/', views.liste_competence, name='liste_competence'),
    path('competence/ajout/', views.competencesCreateView.as_view(), name='competencesCreateView'),
    path('competence/ajout/succes/', views.reussite_ajout_competence, name='reussite_ajout_competence'),
    path('outil/', views.liste_outil_propre, name='liste_outil_propre'),
    path('outil/ajout/', views.outilsCreateView.as_view(), name='outilsCreateView'),
    path('outil/ajout/succes/', views.reussite_ajout_outil, name='reussite_ajout_outil'),
    path('intervention/', views.liste_intervention, name='liste_intervention'),
]