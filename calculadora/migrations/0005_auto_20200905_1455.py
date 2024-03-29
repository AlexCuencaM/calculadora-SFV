# Generated by Django 3.1.1 on 2020-09-05 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculadora', '0004_auto_20200228_1157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalleequipodecomputomodel',
            name='horas',
        ),
        migrations.RemoveField(
            model_name='detalleequipodecomputomodel',
            name='watts',
        ),
        migrations.AddField(
            model_name='detalleequipodecomputomodel',
            name='cantidad',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='detalleequipodecomputomodel',
            name='consumoKwH',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='detalleequipodecomputomodel',
            name='horarios',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='reportemodel',
            name='token',
            field=models.UUIDField(),
            preserve_default=False,
        ),
    ]
