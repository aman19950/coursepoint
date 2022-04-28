# Generated by Django 3.1.14 on 2022-04-07 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('futureskill', '0006_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='prereq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=100)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='futureskill.coursedtls')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='learning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=100)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='futureskill.coursedtls')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
