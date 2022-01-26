# Generated by Django 2.2.5 on 2022-01-26 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('write_date', models.DateTimeField(null=True)),
                ('modify_date', models.DateTimeField(blank=True, null=True)),
                ('content', models.TextField(max_length=255, null=True)),
                ('img_path', models.CharField(max_length=255, null=True)),
                ('reply_count', models.IntegerField(default=0)),
                ('view_count', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bulletin.Post')),
            ],
        ),
    ]
