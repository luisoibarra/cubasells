# Generated by Django 2.2 on 2020-03-27 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0025_auto_20200319_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='Deposit',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='project.BankAccount'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auction',
            name='Password',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auction',
            name='ended',
            field=models.BooleanField(default=False, verbose_name='Ended'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='Winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to='project.BankAccount'),
        ),
    ]
