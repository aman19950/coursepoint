# Generated by Django 3.1.14 on 2022-04-07 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('futureskill', '0004_auto_20220406_2331'),
    ]

    operations = [
        migrations.CreateModel(
            name='coursedtls',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('desc', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('discount', models.IntegerField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('resource', models.FileField(upload_to='files/resource')),
                ('image', models.ImageField(upload_to='files/image')),
            ],
        ),
    ]
