# Generated by Django 3.1.6 on 2021-03-10 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0005_auto_20210310_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentsbook',
            name='quality',
            field=models.CharField(choices=[('0', 'Не указано'), ('1', 'Посредственно'), ('2', 'Неудовлетворительно'), ('3', 'Удовлетворительно'), ('4', 'Хорошо'), ('5', 'Отлично')], default='0', max_length=100, verbose_name='Оценка'),
        ),
    ]
