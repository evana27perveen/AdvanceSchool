# Generated by Django 3.2.13 on 2022-05-15 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentmodel',
            name='batch',
            field=models.CharField(choices=[('17th', '17th'), ('18th', '18th'), ('19th', '19th'), ('20th', '20th'), ('21st', '21st'), ('22nd', '22nd'), ('23rd', '23rd'), ('24th', '24th'), ('25th', '25th'), ('26th', '26th'), ('27th', '27th')], max_length=50),
        ),
        migrations.AlterField(
            model_name='assignmentmodel',
            name='semester',
            field=models.CharField(choices=[('1st', '1st'), ('2nd', '2nd'), ('3rd', '3rd'), ('4th', '4th'), ('5th', '5th'), ('6th', '6th'), ('7th', '7th'), ('8th', '8th')], max_length=50),
        ),
    ]