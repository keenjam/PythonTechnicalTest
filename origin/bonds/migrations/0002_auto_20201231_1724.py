# Generated by Django 2.2.13 on 2020-12-31 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bonds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bond',
            name='legal_name',
            field=models.CharField(blank=True, help_text='Legal name of financial institution', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bond',
            name='lei',
            field=models.CharField(help_text='Legal Entity Field of institution in ISO 17442 code format', max_length=20),
        ),
    ]
