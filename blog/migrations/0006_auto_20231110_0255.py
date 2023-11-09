# Generated by Django 3.2.22 on 2023-11-09 17:55

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20231107_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(storage=blog.models.OverwriteStorage, upload_to=blog.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='user',
            name='pw',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='uid',
            field=models.EmailField(max_length=200, unique=True),
        ),
    ]
