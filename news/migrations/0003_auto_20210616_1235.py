# Generated by Django 3.2.4 on 2021-06-16 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20210616_1223'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postcategory',
            old_name='Category',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='postcategory',
            old_name='Post',
            new_name='post',
        ),
    ]