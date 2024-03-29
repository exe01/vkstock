# Generated by Django 3.0.7 on 2020-07-15 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.IntegerField(default=0)),
                ('platform_id', models.CharField(max_length=256)),
                ('text', models.TextField(blank=True)),
                ('rating', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('token', models.CharField(max_length=256)),
                ('platform_id', models.CharField(blank=True, default='', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('token', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('platform_id', models.CharField(max_length=256)),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock_api.Project')),
                ('type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock_api.Type')),
            ],
        ),
        migrations.CreateModel(
            name='RenderedPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform_id', models.CharField(max_length=256)),
                ('posted_date', models.IntegerField(default=0)),
                ('text', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('AC', 'accepted'), ('UN', 'unaccepted'), ('RE', 'rejected'), ('PO', 'posted')], default='UN', max_length=2)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock_api.Post')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock_api.Project')),
            ],
        ),
        migrations.CreateModel(
            name='RenderedImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='rendered_images')),
                ('rendered_post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='stock_api.RenderedPost')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock_api.Type'),
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='post_images')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='stock_api.Post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='source_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stock_api.Source'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=256)),
                ('text', models.TextField(blank=True, default='')),
                ('ref_text', models.TextField(blank=True, default='')),
                ('rating', models.IntegerField(default=0)),
                ('image', models.ImageField(null=True, upload_to='comment_images')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='stock_api.Post')),
            ],
        ),
    ]
