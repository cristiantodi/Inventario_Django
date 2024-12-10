# Generated by Django 5.1.3 on 2024-12-04 20:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetodoPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='CrearCreadito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('documento', models.PositiveIntegerField()),
                ('registroPago', models.JSONField(default=list)),
                ('producto', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tienda.productos')),
                ('metodoPago', models.ManyToManyField(blank=True, to='credito.metodopago')),
            ],
        ),
    ]