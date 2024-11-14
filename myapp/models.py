from django.db import models

class Site(models.Model):
    SiteID = models.AutoField(primary_key=True)
    Site_num = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.Site