# Generated by Django 5.1.4 on 2024-12-20 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafeauth', '0002_alter_userprofile_phonenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phonenumber',
            field=models.CharField(max_length=15),
        ),
    ]
