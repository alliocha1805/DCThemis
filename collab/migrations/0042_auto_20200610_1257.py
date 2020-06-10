# Generated by Django 3.0.7 on 2020-06-10 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collab', '0041_auto_20200610_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collaborateurs',
            name='clientPrincipaux',
            field=models.ManyToManyField(blank=True, to='collab.client'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='expertiseSectorielle',
            field=models.ManyToManyField(blank=True, to='collab.expertiseSectorielle'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='formation',
            field=models.ManyToManyField(blank=True, to='collab.obtentionFormation'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='langues',
            field=models.ManyToManyField(blank=True, to='collab.LanguesParlee'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='listeCompetencesCles',
            field=models.ManyToManyField(blank=True, to='collab.competences'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='methodologie',
            field=models.ManyToManyField(blank=True, to='collab.Methodo'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='nbAnneeExperience',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='niveauxIntervention',
            field=models.ManyToManyField(blank=True, to='collab.niveauIntervention'),
        ),
        migrations.AlterField(
            model_name='collaborateurs',
            name='outilsCollaborateur',
            field=models.ManyToManyField(blank=True, to='collab.outils'),
        ),
    ]