# Generated by Django 4.0.6 on 2022-08-15 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailsale',
            name='total',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
