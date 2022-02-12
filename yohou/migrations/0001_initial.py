# Generated by Django 3.2.9 on 2022-02-12 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=30)),
                ('category', models.IntegerField(choices=[(1, 'WOMEN'), (2, 'MEN'), (3, 'KIDS')])),
                ('temperature', models.IntegerField()),
                ('weather', models.IntegerField(choices=[(1, '晴れ'), (2, '曇り'), (3, '雨')])),
                ('title', models.CharField(max_length=30)),
                ('text', models.TextField(blank=True, null=True)),
                ('brands_tops', models.CharField(blank=True, max_length=30, null=True)),
                ('brands_bottoms', models.CharField(blank=True, max_length=30, null=True)),
                ('brands_shoes', models.CharField(blank=True, max_length=30, null=True)),
                ('brands_outer', models.CharField(blank=True, max_length=30, null=True)),
                ('brands_accesory', models.CharField(blank=True, max_length=30, null=True)),
                ('photo', models.FileField(upload_to='static/media/posts')),
            ],
        ),
    ]
