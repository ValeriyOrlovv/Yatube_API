# Generated by Django 3.2.16 on 2024-08-17 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20240817_1815'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='self_following_constraint',
        ),
    ]
