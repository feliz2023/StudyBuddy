# Generated by Django 4.2.4 on 2023-09-02 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentHive', '0002_topic_room_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
    ]
