# Generated by Django 3.0.7 on 2020-06-12 09:05

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collab', '0052_auto_20200612_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collaborateurs',
            name='clientPrincipaux',
            field=models.ManyToManyField(blank=True, help_text='Idéalement en indiquer 5 et en ne dépassant pas les 10', to='collab.client', verbose_name='Clients Principaux'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='codePostal',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Code Postal'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='dateDeNaissance',
            field=models.DateField(blank=True, null=True, verbose_name='Date de naissance'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='expSignificative1',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Expérience Significative 1'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='expSignificative2',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Expérience Significative 2'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='expSignificative3',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Expérience Significative 3'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='expSignificative4',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Expérience Significative 4'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='expSignificative5',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Expérience Significative 5'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='expertiseSectorielle',
            field=models.ManyToManyField(blank=True, help_text='Indique le « secteur : Direction ou Service Client » (ex : Industrie Pharmaceutique : Achat, Service Financier)', to='collab.expertiseSectorielle', verbose_name='Expertise Sectorielle'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='langues',
            field=models.ManyToManyField(blank=True, help_text='Obligatoire, indiquez le niveau d’anglais', to='collab.LanguesParlee'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='listeCompetencesCles',
            field=models.ManyToManyField(blank=True, to='collab.competences', verbose_name='Compétences Clés '),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='methodologie',
            field=models.ManyToManyField(blank=True, to='collab.Methodo', verbose_name='Méthodologies'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='nbAnneeExperience',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nb d’année d’expérience'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='niveauxIntervention',
            field=models.ManyToManyField(blank=True, help_text='Idéalement en indiquer 5 et en ne dépassant pas les 10', to='collab.niveauIntervention', verbose_name='Niveau d’intervention'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='outilsCollaborateur',
            field=models.ManyToManyField(blank=True, to='collab.outils', verbose_name='Outils'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='prenomCollaborateur',
            field=models.CharField(max_length=200, verbose_name='Prénom du Collaborateur'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='telephone',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Téléphone'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='texteIntroductifCv',
            field=ckeditor.fields.RichTextField(blank=True, default='', help_text='Il s’agit du texte introductif que l’on retrouve en première page du DC au-dessous du titre introductif', null=True, verbose_name='Texte introductif du DC'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='titreCollaborateur',
            field=models.CharField(help_text='Il s’agit du titre que l’on retrouve en première page du DC au-dessus du texte introductif (ex : Consultant AMOA)', max_length=200, verbose_name='Titre du Collaborateur'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='typeContrat',
            field=models.CharField(choices=[('I', 'CDI'), ('D', 'CDD'), ('N', 'Intérimaire'), ('A', "Contrat d'alternance"), ('X', 'Indépendant'), ('S', 'Sous-traitant')], default='I', max_length=1, verbose_name='Type de Contrat'),
        ),
    ]