# Generated by Django 5.0.1 on 2024-03-10 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_input_history_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='result',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='input',
            name='input_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
