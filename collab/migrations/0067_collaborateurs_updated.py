# Generated by Django 2.2.5 on 2020-07-07 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collab', '0066_auto_20200623_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='collaborateurs',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
