# Generated by Django 3.0.7 on 2020-08-02 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_api', '0003_auto_20200802_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renderedpost',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]