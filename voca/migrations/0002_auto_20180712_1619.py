# Generated by Django 2.0.7 on 2018-07-12 07:19

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('voca', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntryCategoryMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='voca.EntryCategory', verbose_name='entry category')),
            ],
            options={
                'verbose_name': 'category membership',
                'verbose_name_plural': 'category memberships',
            },
        ),
        migrations.RemoveField(
            model_name='entry',
            name='category',
        ),
        migrations.AddField(
            model_name='entrycategorymembership',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voca.Entry'),
        ),
        migrations.AddField(
            model_name='entry',
            name='categories',
            field=models.ManyToManyField(blank=True, through='voca.EntryCategoryMembership', to='voca.EntryCategory'),
        ),
    ]
