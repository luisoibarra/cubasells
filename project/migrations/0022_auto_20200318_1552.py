# Generated by Django 2.2 on 2020-03-18 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0021_auto_20200312_1705'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='Bank account',
            new_name='Bank_Account',
        ),
    ]
