# Generated by Django 4.2.6 on 2023-12-20 12:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
