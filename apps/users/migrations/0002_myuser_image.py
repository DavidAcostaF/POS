# Generated by Django 4.0.6 on 2022-08-12 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='image',
            field=models.ImageField(default=1, upload_to='profile'),
            preserve_default=False,
        ),
    ]
