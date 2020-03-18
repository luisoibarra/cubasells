# Generated by Django 2.2.6 on 2019-11-22 01:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20191122_0044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='Duration(sec)',
            new_name='Duration_in_sec',
        ),
        migrations.RenameField(
            model_name='auction',
            old_name='Initial Date',
            new_name='Initial_Date',
        ),
        migrations.RenameField(
            model_name='bankaccount',
            old_name='Bank account',
            new_name='Bank_account',
        ),
        migrations.RenameField(
            model_name='buyoffer',
            old_name='Buy Date',
            new_name='Buy_Date',
        ),
        migrations.RenameField(
            model_name='offer',
            old_name='Offer description',
            new_name='Offer_description',
        ),
        migrations.RenameField(
            model_name='offer',
            old_name='Offer name',
            new_name='Offer_name',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='Price per unit',
            new_name='Price_per_unit',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='Store Amount',
            new_name='Store_Amount',
        ),
        migrations.AddField(
            model_name='product',
            name='Name',
            field=models.CharField(default=django.utils.timezone.now, max_length=150),
            preserve_default=False,
        ),
    ]