# Generated by Django 3.0.3 on 2020-02-17 02:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculadora', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipodecomputomodel',
            name='horas',
        ),
        migrations.RemoveField(
            model_name='equipodecomputomodel',
            name='watts',
        ),
        migrations.AlterField(
            model_name='equipodecomputomodel',
            name='descripcion',
            field=models.CharField(default='NA', max_length=255),
        ),
        migrations.CreateModel(
            name='DetalleEquipoDeComputoModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watts', models.IntegerField(default=300)),
                ('horas', models.DecimalField(decimal_places=2, default=8, max_digits=10)),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='calculadora.EquipoDeComputoModel')),
            ],
        ),
        migrations.AlterField(
            model_name='consumodedispositivo',
            name='equipo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='calculadora.DetalleEquipoDeComputoModel'),
        ),
    ]