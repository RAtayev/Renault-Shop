# Generated by Django 2.2.1 on 2019-05-21 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20190521_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auto',
            name='image',
            field=models.ImageField(upload_to='autos'),
        ),
    ]
