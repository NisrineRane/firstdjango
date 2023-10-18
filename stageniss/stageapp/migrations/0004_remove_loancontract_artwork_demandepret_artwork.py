# Generated by Django 4.2.5 on 2023-09-17 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stageapp', '0003_demandepret'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loancontract',
            name='artwork',
        ),
        migrations.AddField(
            model_name='demandepret',
            name='artwork',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='stageapp.artwork'),
        ),
    ]
