# Generated by Django 3.1.7 on 2021-04-23 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_category_signers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='signers',
            field=models.ManyToManyField(blank=True, related_name='categories', to='api.Signer'),
        ),
    ]
