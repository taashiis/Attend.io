# Generated by Django 4.0.4 on 2022-05-21 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_session_end_alter_session_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='end',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='start',
            field=models.TimeField(null=True),
        ),
    ]
