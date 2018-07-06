# Generated by Django 2.0.7 on 2018-07-06 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voca', '0002_auto_20180706_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrymeaning',
            name='part',
            field=models.IntegerField(choices=[(0, 'noun'), (1, 'pronoun'), (2, 'verb'), (3, 'modifier'), (4, 'verb'), (5, 'conjunction'), (6, 'interjection')], db_index=True, default=0, verbose_name='part of speech'),
        ),
    ]
