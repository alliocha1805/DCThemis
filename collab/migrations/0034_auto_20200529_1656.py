# Generated by Django 3.0.5 on 2020-05-29 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collab', '0033_auto_20200529_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='languesparlee',
            name='niveau',
            field=models.CharField(choices=[('Debutant', 'Debutant'), ('Courant', 'Courant'), ('Bilingue', 'Bilingue')], default='Debutant', max_length=10),
        ),
    ]
