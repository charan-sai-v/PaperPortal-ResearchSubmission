# Generated by Django 4.2.6 on 2023-10-17 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('maineditor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('token', models.CharField(max_length=255, null=True)),
                ('token_expires_at', models.DateTimeField(null=True)),
                ('password_reset_token', models.CharField(max_length=255, null=True)),
                ('password_reset_token_expires_at', models.DateTimeField(null=True)),
                ('login_token', models.CharField(max_length=255, null=True)),
                ('login_token_expires_at', models.DateTimeField(null=True)),
            ],
            options={
                'verbose_name': 'author',
                'verbose_name_plural': 'authors',
                'db_table': 'author',
            },
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('abstract', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to='papers/')),
                ('status', models.CharField(default='pending', max_length=255)),
                ('no_of_authors', models.IntegerField(default=1)),
                ('author_1', models.CharField(max_length=255)),
                ('author_2', models.CharField(max_length=255, null=True)),
                ('author_3', models.CharField(max_length=255, null=True)),
                ('author_4', models.CharField(max_length=255, null=True)),
                ('author_5', models.CharField(max_length=255, null=True)),
                ('author_6', models.CharField(max_length=255, null=True)),
                ('review_remark_1', models.TextField(null=True)),
                ('review_remark_2', models.TextField(null=True)),
                ('is_review_1_completed', models.BooleanField(default=False)),
                ('is_review_2_completed', models.BooleanField(default=False)),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='author.author')),
                ('conference', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='maineditor.conference')),
                ('maineditor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='maineditor', to='author.author')),
                ('subeditor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subeditor', to='author.author')),
            ],
            options={
                'verbose_name': 'paper',
                'verbose_name_plural': 'papers',
                'db_table': 'paper',
            },
        ),
    ]
