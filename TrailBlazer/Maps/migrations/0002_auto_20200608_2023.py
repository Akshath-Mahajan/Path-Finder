# Generated by Django 3.0.4 on 2020-06-08 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Maps', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nodes',
            old_name='x_coord',
            new_name='latitude',
        ),
        migrations.RenameField(
            model_name='nodes',
            old_name='y_coord',
            new_name='longitude',
        ),
    ]
