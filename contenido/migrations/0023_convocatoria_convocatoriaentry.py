# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-21 20:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0022_denuncia'),
    ]

    operations = [
        migrations.CreateModel(
            name='Convocatoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apertura', models.DateField()),
                ('cierre', models.DateField()),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ConvocatoriaEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('cancion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenido.Audio')),
                ('convocatoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenido.Convocatoria')),
            ],
        ),
    ]