# Generated by Django 4.2.13 on 2024-06-13 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='picture',
            field=models.URLField(blank=True, null=True),
        ),
    ]
