# Generated by Django 2.0.7 on 2018-07-05 14:18

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


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
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('pronunciation', models.CharField(max_length=250, verbose_name='pronunciation')),
                ('status', models.IntegerField(choices=[(0, 'beginner'), (1, 'intermediate'), (2, 'advanced')], db_index=True, default=0, verbose_name='level')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EntryCompound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(verbose_name='position')),
                ('from_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_entry', to='voca.Entry')),
                ('to_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_entry', to='voca.Entry')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='EntryMeaning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('part', models.IntegerField(choices=[(0, 'noun'), (1, 'pronoun'), (2, 'verb'), (3, 'modifier'), (4, 'verb'), (5, 'conjunction'), (6, 'interjection')], db_index=True, default=0, verbose_name='level')),
                ('meaning', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meanings', to='voca.Entry', verbose_name='entry')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='entry',
            name='relationships',
            field=models.ManyToManyField(blank=True, related_name='related_to', through='voca.EntryCompound', to='voca.Entry'),
        ),
    ]
