# Generated by Django 4.1.7 on 2023-03-21 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0003_remove_author_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='password_reset_token',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='password_reset_token_expires_at',
            field=models.DateTimeField(null=True),
        ),
    ]