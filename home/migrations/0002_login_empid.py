# Generated by Django 4.0.4 on 2022-05-10 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='login',
            name='empid',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]
