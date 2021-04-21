# Generated by Django 3.1.7 on 2021-04-21 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210421_1242'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groupsig',
            options={'ordering': ['-created_at'], 'verbose_name': 'groupsig', 'verbose_name_plural': 'groupsigs'},
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requester_address', models.CharField(blank=True, max_length=50, null=True)),
                ('price', models.FloatField(default=0)),
                ('response_time', models.IntegerField(default=0)),
                ('state', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groupsig', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='api.groupsig')),
                ('signer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='api.signer')),
            ],
            options={
                'verbose_name': 'request',
                'verbose_name_plural': 'requests',
                'ordering': ['-created_at'],
            },
        ),
    ]