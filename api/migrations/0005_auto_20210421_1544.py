# Generated by Django 3.1.7 on 2021-04-21 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210421_1500'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request_Signer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signed_at', models.DateTimeField(null=True)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.request')),
                ('signer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.signer')),
            ],
        ),
        migrations.AddField(
            model_name='request',
            name='signers',
            field=models.ManyToManyField(blank=True, related_name='requests', through='api.Request_Signer', to='api.Signer'),
        ),
    ]
