# Generated by Django 3.0.7 on 2020-06-08 15:23

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collab', '0034_auto_20200529_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collaborateurs',
            name='texteIntroductifCv',
            field=ckeditor.fields.RichTextField(default=''),
        ),
    ]
