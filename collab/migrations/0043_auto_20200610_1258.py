# Generated by Django 3.0.7 on 2020-06-10 10:58

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collab', '0042_auto_20200610_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collaborateurs',
            name='parcours',
            field=ckeditor.fields.RichTextField(blank=True, default=''),
        ),
    ]