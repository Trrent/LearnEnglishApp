# Generated by Django 4.2.6 on 2023-12-20 11:16

from django.db import migrations
import users.manager


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_uuid_user_id'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', users.manager.UserManager()),
            ],
        ),
    ]
