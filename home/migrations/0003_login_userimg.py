# Generated by Django 4.0.4 on 2022-05-12 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_login_empid'),
    ]

    operations = [
        migrations.AddField(
            model_name='login',
            name='userimg',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
