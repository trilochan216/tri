# Generated by Django 4.2.7 on 2024-05-09 11:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_alter_mymodel_my_date_field'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyModel',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='address',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='id',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='my_date_field',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='profile',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]