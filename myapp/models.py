from django.db import models
from django.contrib.auth.models import User

class Site(models.Model):
    SiteID = models.AutoField(primary_key=True)
    Site_num = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.Site_num)

class EditorRegistrationCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class EditorTablePermission(models.Model):
    editor = models.ForeignKey(User, on_delete=models.CASCADE)
    table_name = models.CharField(max_length=100)
    can_add = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)  
    can_delete = models.BooleanField(default=False)

    class Meta:
        unique_together = ['editor', 'table_name']