# Generated by Django 3.0.7 on 2020-06-24 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0003_auto_20200624_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mproject',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='skills',
            field=models.TextField(blank=True),
        ),
    ]
