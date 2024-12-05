# Generated by Django 5.1.3 on 2024-12-10 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_create_user_groups'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditorCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('is_used', models.BooleanField(default=False)),
            ],
        ),
    ]