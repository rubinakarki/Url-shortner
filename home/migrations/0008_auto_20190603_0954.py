# Generated by Django 2.2.1 on 2019-06-03 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20190603_0934'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stat',
            old_name='urlinputdetails',
            new_name='url_input_details',
        ),
        migrations.RenameField(
            model_name='urlinput',
            old_name='shortenUrl',
            new_name='shorten_url',
        ),
    ]
