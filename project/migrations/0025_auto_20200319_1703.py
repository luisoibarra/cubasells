# Generated by Django 2.2 on 2020-03-19 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0024_auto_20200319_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='Duration_in_sec',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='auction',
            name='Money',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='Account',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='buyoffer',
            name='Amount',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='Phone',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='Phone',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='suboffer',
            name='Amount',
            field=models.PositiveIntegerField(),
        ),
    ]