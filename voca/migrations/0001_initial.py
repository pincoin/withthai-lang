# Generated by Django 2.0.7 on 2018-07-11 11:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('title', models.CharField(db_index=True, max_length=255, verbose_name='title')),
                ('pronunciation', models.CharField(max_length=250, verbose_name='pronunciation')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('level', models.IntegerField(choices=[(0, 'beginner'), (1, 'intermediate'), (2, 'advanced')], db_index=True, default=0, verbose_name='level')),
            ],
            options={
                'verbose_name': 'entry',
                'verbose_name_plural': 'entries',
            },
        ),
        migrations.CreateModel(
            name='EntryCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('slug', models.SlugField(allow_unicode=True, help_text='A short label containing only letters, numbers, underscores or hyphens for URL', max_length=255, unique=True, verbose_name='slug')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='voca.EntryCategory', verbose_name='parent')),
            ],
            options={
                'verbose_name': 'entry category',
                'verbose_name_plural': 'entry categories',
            },
        ),
        migrations.CreateModel(
            name='EntryCompound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(verbose_name='position')),
                ('from_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='어근', to='voca.Entry')),
                ('to_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='파생어', to='voca.Entry')),
            ],
            options={
                'verbose_name': 'compound word',
                'verbose_name_plural': 'compound words',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='EntryMeaning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('part', models.IntegerField(choices=[(0, 'noun'), (1, 'pronoun'), (2, 'verb'), (3, 'modifier'), (4, 'verb'), (5, 'conjunction'), (6, 'interjection'), (7, 'classifier')], db_index=True, default=0, verbose_name='part of speech')),
                ('meaning', models.CharField(max_length=250, verbose_name='meaning')),
                ('position', models.IntegerField(verbose_name='position')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meanings', to='voca.Entry', verbose_name='entry')),
            ],
            options={
                'verbose_name': 'meaning',
                'verbose_name_plural': 'meanings',
                'ordering': ['position'],
            },
        ),
        migrations.AddField(
            model_name='entry',
            name='category',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='표제어', to='voca.EntryCategory', verbose_name='entry category'),
        ),
        migrations.AddField(
            model_name='entry',
            name='relationships',
            field=models.ManyToManyField(blank=True, related_name='components', through='voca.EntryCompound', to='voca.Entry'),
        ),
    ]
