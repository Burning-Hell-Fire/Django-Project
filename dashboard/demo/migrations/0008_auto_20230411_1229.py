# Generated by Django 3.2.18 on 2023-04-11 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0007_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='image',
            field=models.ImageField(default='default_image.png', null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(default='default_image.png', null=True, upload_to='image/'),
        ),
    ]
