# Generated by Django 4.1 on 2023-07-23 22:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TipoDeTecnologia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Tipo De Tecnología',
                'verbose_name_plural': 'Tipos De Tecnologías',
            },
        ),
        migrations.CreateModel(
            name='Tecnologia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('Imagen', models.ImageField(blank=True, null=True, upload_to='Tecnologias')),
                ('accionEsperada', models.CharField(max_length=255, verbose_name='Acción Esperada')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('tipoDeTecnologia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TECNOLOGIAS.tipodetecnologia', verbose_name='Tipo')),
            ],
            options={
                'verbose_name': 'Tecnología',
                'verbose_name_plural': 'Tecnologías',
            },
        ),
        migrations.CreateModel(
            name='Especie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreCientifico', models.CharField(max_length=255, verbose_name='Nombre Científico')),
                ('nombreComun', models.CharField(max_length=255, verbose_name='Nombre Común')),
                ('tipoDeTecnologia', models.CharField(choices=[('animal', 'animal'), ('vegetal', 'vegetal')], default='animal', max_length=10)),
                ('tecnologias', models.ManyToManyField(to='TECNOLOGIAS.tecnologia')),
            ],
            options={
                'verbose_name': 'Especie',
                'verbose_name_plural': 'Especies',
            },
        ),
    ]
