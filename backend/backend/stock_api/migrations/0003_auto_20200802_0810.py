# Generated by Django 3.0.7 on 2020-08-02 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock_api', '0002_auto_20200802_0758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='renderedpost',
            old_name='likes',
            new_name='rating',
        ),
    ]
