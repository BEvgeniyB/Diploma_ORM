# Generated by Django 5.1.2 on 2024-11-07 16:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(db_index=True, max_length=15)),
                ('firstname', models.CharField(max_length=15)),
                ('lastname', models.CharField(max_length=15)),
                ('age', models.IntegerField()),
                ('slug', models.CharField(db_index=True, max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=250)),
                ('content', models.TextField()),
                ('priority', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('slug', models.CharField(db_index=True, max_length=15)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to='app.user')),
            ],
        ),
    ]