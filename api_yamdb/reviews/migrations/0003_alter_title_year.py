# Generated by Django 3.2 on 2023-10-08 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveIntegerField(verbose_name='Год выпуска'),
        ),
    ]
