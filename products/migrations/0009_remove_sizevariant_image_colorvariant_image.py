# Generated by Django 4.2.7 on 2024-04-06 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_sizevariant_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sizevariant',
            name='image',
        ),
        migrations.AddField(
            model_name='colorvariant',
            name='image',
            field=models.ImageField(default=True, upload_to=''),
        ),
    ]
