# Generated by Django 3.2.9 on 2022-02-13 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yohou', '0005_post_brands_onpiece'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(upload_to='static/media/posts'),
        ),
    ]