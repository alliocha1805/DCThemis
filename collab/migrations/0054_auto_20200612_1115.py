# Generated by Django 3.0.7 on 2020-06-12 09:15

import ckeditor.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collab', '0053_auto_20200612_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiences',
            name='employeur',
            field=models.CharField(blank=True, default='', help_text='Dans le cas où la coche est décochée, merci d’indiquer pour le compte de quelle société avez-vous effectué cette intervention ?', max_length=300, verbose_name='Employeur lors de l’interventio'),
        ),
        migrations.AlterField(
            model_name='experiences',
            name='collaborateurMission',
            field=models.ForeignKey(default='', help_text='Utilisez la liste pour rattacher le collaborateur à la mission', on_delete=django.db.models.deletion.CASCADE, to='collab.collaborateurs', verbose_name='Collaborateur'),
        ),
        migrations.AlterField(
            model_name='experiences',
            name='descriptifMission',
            field=ckeditor.fields.RichTextField(blank=True, default='', help_text='Décrire l’intervention en détail', verbose_name='Descriptif de la mission'),
        ),
        migrations.AlterField(
            model_name='experiences',
            name='environnementMission',
            field=ckeditor.fields.RichTextField(blank=True, default='', null=True, verbose_name='Environnement Technique'),
        ),
        migrations.AlterField(
            model_name='experiences',
            name='mandataire',
            field=models.CharField(blank=True, default='', help_text='Si vous êtes passez par un intermédiaire, merci d’indiquer le nom de la société sous-traitante (ex :Eugena)', max_length=300),
        ),
        migrations.AlterField(
            model_name='experiences',
            name='missionThemis',
            field=models.BooleanField(default=True, help_text='Décochez la coche, s’il s’agit d’une mission pour le compte d’une autre société'),
        ),
        migrations.AlterField(
            model_name='experiences',
            name='nomMission',
            field=models.CharField(help_text='Indiquez le poste occupé par le consultant lors de l’intervention ex : (Consultant BI)', max_length=300, verbose_name='Niveau d’intervention'),
        ),
        migrations.AlterField(
            model_name='experiences',
            name='pourcentageIntervention',
            field=models.IntegerField(blank=True, default=100, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)], verbose_name='Pourcentage du temps passé en intervention'),
        ),
        migrations.AlterField(
            model_name='experiences',
            name='projetDeLaMission',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='collab.projet', verbose_name='Projet de la mission'),
        ),
        migrations.AlterField(
            model_name='experiences',
            name='resumeIntervention',
            field=ckeditor.fields.RichTextField(blank=True, default='', verbose_name='Contexte de l’intervention'),
        ),
        migrations.AlterField(
            model_name='experiences',
            name='service',
            field=models.CharField(blank=True, default='', help_text='Indiquez le la Direction ou le Service du client dans lequel le consultant est intervenu', max_length=300, verbose_name='Direction ou Service Client'),
        ),
    ]
