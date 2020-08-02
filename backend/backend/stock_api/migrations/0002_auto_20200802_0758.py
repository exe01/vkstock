# Generated by Django 3.0.7 on 2020-08-02 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='rating',
            new_name='likes',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='rating',
            new_name='likes',
        ),
        migrations.AddField(
            model_name='renderedpost',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='source',
            name='members',
            field=models.IntegerField(default=0),
        ),
    ]