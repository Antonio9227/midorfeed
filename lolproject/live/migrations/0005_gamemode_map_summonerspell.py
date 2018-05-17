# Generated by Django 2.0.5 on 2018-05-17 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('live', '0004_auto_20180513_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameMode',
            fields=[
                ('mode', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SummonerSpell',
            fields=[
                ('key', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=150)),
            ],
        ),
    ]