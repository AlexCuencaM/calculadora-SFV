# Generated by Django 3.0.3 on 2020-02-17 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculadora', '0002_auto_20200216_2102'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipodecomputomodel',
            options={'ordering': ['descripcion']},
        ),
    ]
