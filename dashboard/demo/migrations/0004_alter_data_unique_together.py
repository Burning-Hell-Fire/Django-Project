# Generated by Django 3.2.18 on 2023-04-06 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0003_alter_data_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='data',
            unique_together=set(),
        ),
    ]