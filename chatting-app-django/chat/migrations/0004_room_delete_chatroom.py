# Generated by Django 4.0.4 on 2022-05-14 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_chatroom'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='ChatRoom',
        ),
    ]
