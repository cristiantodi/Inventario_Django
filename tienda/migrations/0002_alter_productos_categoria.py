# Generated by Django 5.1.2 on 2024-10-21 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='categoria',
            field=models.ManyToManyField(blank=True, null=True, to='tienda.categoria'),
        ),
    ]
