# Generated by Django 3.0.4 on 2020-04-08 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0029_auto_20200408_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='Message',
            field=models.CharField(max_length=999),
        ),
    ]
