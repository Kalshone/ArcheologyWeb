from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def create_groups(apps, schema_editor):
    # Create editor group
    editor_group, created = Group.objects.get_or_create(name='Editor')
    
    # Initially editors have no permissions
    editor_group.permissions.clear()

def delete_groups(apps, schema_editor):
    Group.objects.filter(name='Editor').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups, delete_groups),
    ]