# Generated by Django 2.2.16 on 2020-10-04 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Galeria',
            fields=[
                ('codigo', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
            ],
        ),
    ]
