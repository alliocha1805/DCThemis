# Generated by Django 3.0.5 on 2020-05-29 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collab', '0026_delete_langue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collaborateurs',
            name='typeContrat',
            field=models.CharField(blank=True, choices=[('I', 'CDI'), ('D', 'CDD'), ('N', 'Intérimaire'), ('A', "Contrat d'alternance"), ('X', 'Indépendant'), ('S', 'Sous-traitant')], default='I', max_length=1, null=True),
        ),
    ]
