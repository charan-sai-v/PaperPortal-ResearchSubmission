# Generated by Django 4.2.6 on 2023-10-18 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maineditor', '0001_initial'),
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'contact',
                'verbose_name_plural': 'contacts',
                'db_table': 'contact',
            },
        ),
        migrations.AlterField(
            model_name='paper',
            name='maineditor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='maineditor', to='maineditor.maineditor'),
        ),
    ]
