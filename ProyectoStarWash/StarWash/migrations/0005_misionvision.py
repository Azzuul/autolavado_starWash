# Generated by Django 2.2.16 on 2020-10-13 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StarWash', '0004_auto_20201013_1843'),
    ]

    operations = [
        migrations.CreateModel(
            name='MisionVision',
            fields=[
                ('nombre', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('mision', models.TextField()),
                ('vision', models.TextField()),
            ],
        ),
    ]
