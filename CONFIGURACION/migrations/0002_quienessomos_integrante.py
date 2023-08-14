# Generated by Django 4.1 on 2023-08-14 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CONFIGURACION', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuienesSomos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Titulo', models.CharField(max_length=255)),
                ('SubTitulo', models.CharField(max_length=255, verbose_name='Sub Título')),
                ('Imagen', models.ImageField(upload_to='Quienes_Somos')),
                ('Descripcion', models.TextField()),
                ('DescripcionNuestroEquipo', models.TextField(verbose_name='Nuestro Equipo')),
            ],
            options={
                'verbose_name': 'Quienes Somos',
                'verbose_name_plural': 'Quienes Somos',
            },
        ),
        migrations.CreateModel(
            name='Integrante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=255)),
                ('Categoria', models.CharField(max_length=255)),
                ('Imagen', models.ImageField(upload_to='Quienes_Somos_Integrantes')),
                ('Descripcion', models.TextField()),
                ('Pagina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CONFIGURACION.quienessomos')),
            ],
            options={
                'verbose_name': 'Quienes Somos',
                'verbose_name_plural': 'Quienes Somos',
            },
        ),
    ]
