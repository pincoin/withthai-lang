# Generated by Django 2.0.7 on 2018-07-23 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voca', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='textbook',
            name='status',
            field=models.IntegerField(choices=[(0, 'public'), (1, 'private')], db_index=True, default=0, verbose_name='status'),
        ),
    ]
