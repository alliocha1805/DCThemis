# Generated by Django 2.2.5 on 2020-07-23 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collab', '0067_collaborateurs_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiences',
            name='contactClient1',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='experiences',
            name='contactClient2',
            field=models.TextField(blank=True, default=''),
        ),
    ]
