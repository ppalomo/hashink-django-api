# Generated by Django 3.1.7 on 2021-04-27 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20210424_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='signer',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='signer',
            name='number_of_prints',
            field=models.IntegerField(default=0),
        ),
    ]
