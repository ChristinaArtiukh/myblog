# Generated by Django 3.1.6 on 2021-03-01 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='authorinfo',
            name='name',
            field=models.CharField(blank=True, max_length=150, verbose_name='Имя'),
        ),
    ]
