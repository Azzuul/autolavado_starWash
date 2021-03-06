# Generated by Django 2.2.16 on 2020-10-13 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StarWash', '0005_misionvision'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mision',
            fields=[
                ('nombre', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('mision', models.TextField()),
                ('imagen', models.ImageField(null=True, upload_to='misionVision')),
            ],
        ),
        migrations.CreateModel(
            name='Vision',
            fields=[
                ('nombre', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('mision', models.TextField()),
                ('imagen', models.ImageField(null=True, upload_to='misionVision')),
            ],
        ),
        migrations.DeleteModel(
            name='MisionVision',
        ),
    ]
