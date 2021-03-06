# Generated by Django 2.1.4 on 2018-12-27 14:16

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('article_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('date_edited', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(max_length=50)),
                ('dscr', models.CharField(max_length=255)),
                ('content', tinymce.models.HTMLField()),
                ('thumb', models.FileField(default='article.png', upload_to='article')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.AutoField(primary_key=True, serialize=False)),
                ('ord', models.PositiveIntegerField(default=0)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('date_edited', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(max_length=100)),
                ('writer', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=4)),
                ('dscr', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('thumb', models.FileField(default='book.png', upload_to='book')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('cat_id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('a', 'article'), ('b', 'book'), ('l', 'link')], max_length=1)),
                ('ord', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=50)),
                ('dscr', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('gallery_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('date_edited', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(max_length=50)),
                ('dscr', tinymce.models.HTMLField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='web.Gallery')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('image_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('date_edited', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(max_length=50)),
                ('dscr', tinymce.models.HTMLField()),
                ('image', models.FileField(default='image.png', upload_to='image')),
                ('ord', models.PositiveIntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='web.Gallery')),
                ('next', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='nextImage', to='web.Image')),
                ('prev', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='prevImage', to='web.Image')),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('link_id', models.AutoField(primary_key=True, serialize=False)),
                ('ord', models.PositiveIntegerField(default=0)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('date_edited', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=4)),
                ('dscr', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('thumb', models.FileField(default='link.png', upload_to='link')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='web.Category')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='web.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='web.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='gallery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='web.Gallery'),
        ),
    ]
