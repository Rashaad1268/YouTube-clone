# Generated by Django 3.1.7 on 2021-03-15 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_auto_20210315_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creatorprofile',
            name='profile_picture',
            field=models.ImageField(default='pictures/profile_pic.jpg', upload_to='images/profile_pics'),
        ),
    ]
