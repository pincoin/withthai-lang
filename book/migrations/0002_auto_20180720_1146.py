# Generated by Django 2.0.7 on 2018-07-20 02:46

import book.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import easy_thumbnails.fields
import model_utils.fields
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, verbose_name='title')),
                ('description', models.CharField(blank=True, help_text="A short description not longer than 155 characters. Don't use double quotes.", max_length=255, verbose_name='description')),
                ('keywords', models.CharField(blank=True, help_text="A comma-separated list of keywords. Don't use double quotes.", max_length=255, verbose_name='keywords')),
                ('content', models.TextField(verbose_name='content')),
                ('content1', models.TextField(blank=True, verbose_name='content1')),
                ('content2', models.TextField(blank=True, verbose_name='content2')),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(blank=True, upload_to=book.models.upload_directory_path, verbose_name='image')),
                ('youtube', models.URLField(blank=True, verbose_name='youtube')),
                ('status', models.IntegerField(choices=[(0, 'draft'), (1, 'public'), (2, 'private')], db_index=True, default=1, verbose_name='status')),
                ('view_count', models.PositiveIntegerField(default=0, verbose_name='view count')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP address')),
                ('updated', models.DateTimeField(null=True, verbose_name='updated date')),
            ],
            options={
                'verbose_name': 'article',
                'verbose_name_plural': 'articles',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('slug', models.SlugField(allow_unicode=True, help_text='A short label containing only letters, numbers, underscores or hyphens for URL', max_length=255, unique=True, verbose_name='slug')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='book.ArticleCategory', verbose_name='parent')),
            ],
            options={
                'verbose_name': 'article category',
                'verbose_name_plural': 'article categories',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='book.ArticleCategory', verbose_name='article category'),
        ),
        migrations.AddField(
            model_name='article',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book_article_owned', to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
    ]