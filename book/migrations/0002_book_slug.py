# Generated by Django 2.0.7 on 2018-07-21 09:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='slug',
            field=models.SlugField(allow_unicode=True, default=django.utils.timezone.now, help_text='A short label containing only letters, numbers, underscores or hyphens for URL', max_length=255, verbose_name='slug'),
            preserve_default=False,
        ),
    ]
