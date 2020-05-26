# Generated by Django 3.0.5 on 2020-05-26 15:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('collab', '0016_auto_20200526_1656'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collaborateurs',
            name='manager',
        ),
        migrations.CreateModel(
            name='gestionManagerialeConsultant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateDebut', models.DateField(null=True, verbose_name='date de début de la gestion du consultant')),
                ('dateFin', models.DateField(blank=True, null=True, verbose_name='date de fin de la gestion du consultant')),
                ('manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='collaborateurs',
            name='manager',
            field=models.ManyToManyField(to='collab.gestionManagerialeConsultant'),
        ),
    ]