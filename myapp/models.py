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

class SiteType(models.TextChoices):
    SETTLEMENT = 'ST', 'Settlement'
    BURIAL = 'BG', 'Burial Ground'
    RELIGIOUS = 'RS', 'Religious Site'
    MILITARY = 'MS', 'Military Structure'
    AGRICULTURAL = 'AS', 'Agricultural Site'
    INDUSTRIAL = 'IS', 'Industrial Site'
    ROCK_ART = 'RA', 'Rock Art Site'
    UNDERWATER = 'UW', 'Underwater Site'

class TerrainType(models.TextChoices):
    COASTAL = 'CO', 'Coastal'
    DESERT = 'DE', 'Desert'
    FOREST = 'FO', 'Forest'
    GRASSLAND = 'GR', 'Grassland'
    MOUNTAIN = 'MT', 'Mountain'
    RIVER = 'RV', 'River Valley'
    URBAN = 'UR', 'Urban'
    WETLAND = 'WE', 'Wetland'

class ConditionType(models.TextChoices):
    DESTROYED = 'DS', 'Destroyed'
    HEAVY_DAMAGE = 'HD', 'Heavily Damaged'
    PARTIAL_DAMAGE = 'PD', 'Partially Damaged'
    FAIR = 'FR', 'Fair Condition'
    GOOD = 'GD', 'Good Condition'
    INTACT = 'IN', 'Fully Intact'

class VisibilityType(models.TextChoices):
    NOT_VISIBLE = 'NV', 'Not Visible'
    POOR = 'PR', 'Poor (<25%)'
    FAIR = 'FR', 'Fair (25-50%)'
    GOOD = 'GD', 'Good (50-75%)'
    EXCELLENT = 'EX', 'Excellent (>75%)'

class Sites(models.Model):
    siteNo = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=6, decimal_places=4)
    longitude = models.DecimalField(max_digits=7, decimal_places=4)
    length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    type = models.CharField(
        max_length=2,
        choices=SiteType.choices,
        null=False,
        blank=False
    )
    terrain = models.CharField(
        max_length=2,
        choices=TerrainType.choices,
        null=False,
        blank=False
    )
    condition = models.CharField(
        max_length=2,
        choices=ConditionType.choices,
        default=ConditionType.FAIR
    )
    stratification = models.PositiveIntegerField(null=True, blank=True)
    surfaceVisibility = models.CharField(
        max_length=2,
        choices=VisibilityType.choices,
        default=VisibilityType.FAIR
    )
    elevation = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"{self.siteNo} - {self.name}"