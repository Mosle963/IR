# Generated by Django 5.1.3 on 2024-12-01 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='termdocument',
            name='positions',
        ),
        migrations.AlterField(
            model_name='document',
            name='question',
            field=models.TextField(),
        ),
    ]
