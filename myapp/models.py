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

# SITE DROPDOWNS
class SiteType(models.TextChoices):
    SETTLEMENT = 'ST', 'Settlement'
    BURIAL = 'BG', 'Burial Ground'
    RELIGIOUS = 'RS', 'Religious Site'
    MILITARY = 'MS', 'Military Structure'
    AGRICULTURAL = 'AS', 'Agricultural Site'
    INDUSTRIAL = 'IS', 'Industrial Site'
    ROCK_ART = 'RA', 'Rock Art Site'
    UNDERWATER = 'UW', 'Underwater Site'
    LITHIC_SCATTER = 'LS', 'Lithic Scatter'
    SHERD_SCATTER = 'SS', 'Sherd Scatter'
    CEMETERY = 'CE', 'Cemetery'
    TOMB = 'TB', 'Tomb or Cemetery'
    KHIRBAH = 'KH', 'Khirbah'

class TerrainType(models.TextChoices):
    HILL = 'HL', 'Hill'
    SLOPE = 'SL', 'Slope'
    RIDGE = 'RD', 'Ridge'
    VALLEY = 'VL', 'Valley'
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
    PASTURE = 'PS', 'Pasture'
    PLOWED_FIELD = 'PF', 'Plowed field'

class VisibilityType(models.TextChoices):
    NOT_VISIBLE = 'NV', 'Not Visible'
    POOR = 'PR', 'Poor (<25%)'
    FAIR = 'FR', 'Fair (25-50%)'
    GOOD = 'GD', 'Good (50-75%)'
    EXCELLENT = 'EX', 'Excellent (>75%)'

    BARE_ROCK = 'BR', 'Bare Rock'
    CULTIVATED = 'CU', 'Cultivated'
    BARE_ROCK_CULT = 'BC', 'Bare rock, cult.'
    REGULAR = 'RG', 'Regular'

# LOCI DROPDOWNS
class LociType(models.TextChoices):
    SOIL = 'SL', 'Soil'
    SURFACE = 'SF', 'Surface'
    COLLAPSE = 'CL', 'Collapse'
    PIT_FILL = 'PF', 'Pit fill'
    WALL_STONE = 'WS', 'Wall/Stone feature'
    VIRGIN_SOIL = 'VS', 'Virgin Soil'
    BAULK_TRIM = 'BT', 'Baulk trim'
    OTHER = 'OT', 'Other'

class TextureType(models.TextChoices):
    CLAY = 'CL', 'Clay'
    SILT = 'SL', 'Silt'
    SAND = 'SD', 'Sand'
    LOAM = 'LM', 'Loam'
    SANDY_CLAY = 'SC', 'Sandy Clay'
    SILTY_CLAY = 'SLC', 'Silty Clay'
    SANDY_LOAM = 'SLM', 'Sandy Loam'
    SILTY_LOAM = 'SILM', 'Silty Loam'

class InclusionType(models.TextChoices):
    TREE_ROOTS = 'TR', 'Tree Roots'
    ASH = 'AS', 'Ash'
    CHARCOAL = 'CH', 'Charcoal'
    BRICK = 'BR', 'Brick'
    BONE = 'BO', 'Bone'
    SHELL = 'SH', 'Shell'
    POTTERY = 'PO', 'Pottery'
    STONE = 'ST', 'Stone'

class RoundnessType(models.TextChoices):
    COBBLE = 'CB', 'Cobble'
    PEBBLE = 'PB', 'Pebble'
    ANGULAR = 'AN', 'Angular'
    SUBANGULAR = 'SA', 'Subangular'
    ROUNDED = 'RD', 'Rounded'
    WELL_ROUNDED = 'WR', 'Well Rounded'

class DensityType(models.TextChoices):
    LOW = 'LW', 'Low'
    MODERATE = 'MD', 'Moderate'
    HIGH = 'HI', 'High'
    VERY_HIGH = 'VH', 'Very High'


# CERAMICS DROPDOWNS
class PotteryType(models.TextChoices):
    RIM = 'RM', 'Rim'
    BASE = 'BS', 'Base'
    HANDLE = 'HD', 'Handle'
    BODY = 'BD', 'Body'
    NECK = 'NK', 'Neck'
    SHOULDER = 'SH', 'Shoulder'
    SPOUT = 'SP', 'Spout'
    COMPLETE = 'CP', 'Complete Vessel'

# Pottery Rim choices
class RimFormType(models.TextChoices):
    EVERTED = 'EV', 'Everted'
    INVERTED = 'IN', 'Inverted'
    STRAIGHT = 'ST', 'Straight'
    LEDGED = 'LD', 'Ledged'
    COLLARED = 'CO', 'Collared'
    FLANGED = 'FL', 'Flanged'

class RimStanceType(models.TextChoices):
    VERTICAL = 'VT', 'Vertical'
    FLARING = 'FL', 'Flaring'
    RESTRICTED = 'RS', 'Restricted'
    CLOSED = 'CL', 'Closed'
    OPEN = 'OP', 'Open'

class RimProfileType(models.TextChoices):
    ROUNDED = 'RD', 'Rounded'
    SQUARED = 'SQ', 'Squared'
    POINTED = 'PT', 'Pointed'
    THICKENED = 'TH', 'Thickened'
    BEVELLED = 'BV', 'Bevelled'

class LipShapeType(models.TextChoices):
    FLAT = 'FL', 'Flat'
    ROUNDED = 'RD', 'Rounded'
    POINTED = 'PT', 'Pointed'
    THICKENED = 'TH', 'Thickened'
    TAPERED = 'TP', 'Tapered'

class SymmetryType(models.TextChoices):
    SYMMETRIC = 'SY', 'Symmetric'
    ASYMMETRIC = 'AS', 'Asymmetric'

# Pottery Base choices
class BaseFormType(models.TextChoices):
    FLAT = 'FL', 'Flat'
    ROUNDED = 'RD', 'Rounded'
    RING = 'RG', 'Ring'
    DISK = 'DK', 'Disk'
    PEDESTAL = 'PD', 'Pedestal'
    FOOTED = 'FT', 'Footed'

class BaseStanceType(models.TextChoices):
    STABLE = 'ST', 'Stable'
    UNSTABLE = 'UN', 'Unstable'
    RAISED = 'RA', 'Raised'

class BaseProfileType(models.TextChoices):
    FLAT = 'FL', 'Flat'
    CONCAVE = 'CV', 'Concave'
    CONVEX = 'CX', 'Convex'
    POINTED = 'PT', 'Pointed'

class BaseJunctionType(models.TextChoices):
    CONTINUOUS = 'CT', 'Continuous'
    ANGLED = 'AG', 'Angled'
    CARINATED = 'CR', 'Carinated'
    STEPPED = 'ST', 'Stepped'

# Pottery Handle choices
class HandleTypeType(models.TextChoices):
    LOOP = 'LP', 'Loop'
    STRAP = 'ST', 'Strap'
    LUG = 'LG', 'Lug'
    KNOB = 'KB', 'Knob'
    TAB = 'TB', 'Tab'
    WISHBONE = 'WB', 'Wishbone'
    BASKET = 'BK', 'Basket'

class HandleSectionType(models.TextChoices):
    ROUND = 'RD', 'Round'
    OVAL = 'OV', 'Oval'
    RECTANGULAR = 'RC', 'Rectangular'
    SQUARED = 'SQ', 'Squared'
    FLATTENED = 'FL', 'Flattened'
    GROOVED = 'GR', 'Grooved'
    TWISTED = 'TW', 'Twisted'

class HandleAttachmentType(models.TextChoices):
    RIM_TO_BODY = 'RB', 'Rim to Body'
    RIM_TO_SHOULDER = 'RS', 'Rim to Shoulder'
    SHOULDER_TO_BODY = 'SB', 'Shoulder to Body'
    BODY_TO_BODY = 'BB', 'Body to Body'
    SINGLE_ATTACHMENT = 'SA', 'Single Attachment'


# LITHICS DROPDOWNS
class CoreCodeType(models.TextChoices):
    SINGLE_PLATFORM = 'SP', 'Single Platform'
    MULTIPLE_PLATFORM = 'MP', 'Multiple Platform'
    BIPOLAR = 'BP', 'Bipolar'
    DISCOIDAL = 'DC', 'Discoidal'
    PYRAMIDAL = 'PY', 'Pyramidal'
    PRISMATIC = 'PR', 'Prismatic'
    TESTED = 'TS', 'Tested'
    EXHAUSTED = 'EX', 'Exhausted'

class CoreType(models.TextChoices):
    FLAKE = 'FL', 'Flake'
    BLADE = 'BL', 'Blade'
    MIXED = 'MX', 'Mixed'
    LEVALLOIS = 'LV', 'Levallois'
    MICROBLADE = 'MB', 'Microblade'
    BIFACE = 'BF', 'Biface'

class PlatformCodeType(models.TextChoices):
    PLAIN = 'PL', 'Plain'
    FACETED = 'FC', 'Faceted'
    DIHEDRAL = 'DH', 'Dihedral'
    CORTICAL = 'CT', 'Cortical'
    CRUSHED = 'CR', 'Crushed'
    PUNCTIFORM = 'PF', 'Punctiform'
    LINEAR = 'LN', 'Linear'

class PlatformType(models.TextChoices):
    FLAT = 'FL', 'Flat'
    ANGLED = 'AN', 'Angled'
    CONVEX = 'CV', 'Convex'
    CONCAVE = 'CC', 'Concave'
    IRREGULAR = 'IR', 'Irregular'

class PlatformPrepType(models.TextChoices):
    NONE = 'NO', 'None'
    ABRASION = 'AB', 'Abrasion'
    ISOLATION = 'IS', 'Isolation'
    FACETING = 'FC', 'Faceting'
    COMPLETE = 'CP', 'Complete'

class StageOfUseType(models.TextChoices):
    INITIAL = 'IN', 'Initial'
    INTERMEDIATE = 'IM', 'Intermediate'
    EXHAUSTED = 'EX', 'Exhausted'
    RECYCLED = 'RC', 'Recycled'

class RawMaterialType(models.TextChoices):
    CHERT = 'CT', 'Chert'
    FLINT = 'FL', 'Flint'
    OBSIDIAN = 'OB', 'Obsidian'
    QUARTZ = 'QZ', 'Quartz'
    QUARTZITE = 'QT', 'Quartzite'
    BASALT = 'BS', 'Basalt'
    LIMESTONE = 'LS', 'Limestone'
    SANDSTONE = 'SS', 'Sandstone'
    JASPER = 'JP', 'Jasper'
    CHALCEDONY = 'CH', 'Chalcedony'
    RHYOLITE = 'RH', 'Rhyolite'
    OTHER = 'OT', 'Other'

class GeologicalConditionType(models.TextChoices):
    PRISTINE = 'PR', 'Pristine'
    WEATHERED = 'WE', 'Weathered'
    PATINATED = 'PT', 'Patinated'
    ROLLED = 'RL', 'Rolled'
    THERMAL_DAMAGE = 'TD', 'Thermal Damage'
    CHEMICAL_ALTERATION = 'CA', 'Chemical Alteration'

class BladeCodeType(models.TextChoices):
    PRIMARY = 'PR', 'Primary'
    SECONDARY = 'SC', 'Secondary'
    TERTIARY = 'TR', 'Tertiary'
    CRESTED = 'CR', 'Crested'
    PLUNGING = 'PL', 'Plunging'
    HINGED = 'HI', 'Hinged'
    OVERSHOT = 'OS', 'Overshot'

class ToolTypeType(models.TextChoices):
    SCRAPER = 'SC', 'Scraper'
    BURIN = 'BR', 'Burin'
    POINT = 'PT', 'Point'
    BIFACE = 'BF', 'Biface'
    KNIFE = 'KN', 'Knife'
    MICROLITH = 'MC', 'Microlith'
    PERFORATOR = 'PF', 'Perforator'
    NOTCH = 'NT', 'Notch'
    DENTICULATE = 'DN', 'Denticulate'
    AXE = 'AX', 'Axe'
    ARROWHEAD = 'AR', 'Arrowhead'
    OTHER = 'OT', 'Other'

class HammerType(models.TextChoices):
    YES = 'Y', 'Yes'
    NO = 'N', 'No'
    INDETERMINATE = 'I', 'Indeterminate'

class BackingCodeType(models.TextChoices):
    NONE = 'NO', 'None'
    PARTIAL = 'PA', 'Partial'
    COMPLETE = 'CP', 'Complete'
    ALTERNATE = 'AL', 'Alternate'
    BIFACIAL = 'BF', 'Bifacial'

class BackingTypeType(models.TextChoices):
    NONE = 'NO', 'None'
    ABRUPT = 'AB', 'Abrupt'
    SEMI_ABRUPT = 'SA', 'Semi-abrupt'
    INVASIVE = 'IV', 'Invasive'
    PRESSURE = 'PR', 'Pressure'

class RetouchCodeType(models.TextChoices):
    NONE = 'NO', 'None'
    MARGINAL = 'MG', 'Marginal'
    INVASIVE = 'IV', 'Invasive'
    COVERING = 'CV', 'Covering'
    STEPPED = 'ST', 'Stepped'

class RetouchTypeType(models.TextChoices):
    NONE = 'NO', 'None'
    SCALAR = 'SC', 'Scalar'
    PARALLEL = 'PA', 'Parallel'
    SUBPARALLEL = 'SP', 'Subparallel'
    DENTICULATED = 'DN', 'Denticulated'
    NOTCHED = 'NT', 'Notched'
    PRESSURE = 'PR', 'Pressure'

class UseWearResultType(models.TextChoices):
    NONE = 'NO', 'None'
    CUTTING = 'CT', 'Cutting'
    SCRAPING = 'SC', 'Scraping'
    BORING = 'BO', 'Boring'
    CHOPPING = 'CH', 'Chopping'
    POUNDING = 'PO', 'Pounding'
    MIXED = 'MX', 'Mixed'
    INDETERMINATE = 'IN', 'Indeterminate'

class DebitageCodeType(models.TextChoices):
    FLAKE = 'FL', 'Flake'
    BLADE = 'BL', 'Blade'
    BLADELET = 'BT', 'Bladelet'
    CHUNK = 'CH', 'Chunk'
    CHIP = 'CP', 'Chip'
    SHATTER = 'SH', 'Shatter'
    CORE_TRIMMING = 'CT', 'Core Trimming'
    BURIN_SPALL = 'BS', 'Burin Spall'

class DebitageTypeType(models.TextChoices):
    PRIMARY = 'PR', 'Primary (>50% cortex)'
    SECONDARY = 'SC', 'Secondary (<50% cortex)'
    TERTIARY = 'TR', 'Tertiary (no cortex)'
    CORE_REJUVENATION = 'CR', 'Core Rejuvenation'
    TECHNICAL = 'TC', 'Technical Piece'


# METALS AND SPECIAL FINDS DROPDOWNS
class MetalType(models.TextChoices):
    GOLD = 'GD', 'Gold'
    SILVER = 'SV', 'Silver'
    COPPER = 'CP', 'Copper'
    BRONZE = 'BZ', 'Bronze'
    IRON = 'IR', 'Iron'
    OTHER = 'OT', 'Other'

class MetalArtifactType(models.TextChoices):
    COIN = 'CN', 'Coin'
    JEWELRY = 'JW', 'Jewelry'
    TOOL = 'TL', 'Tool'
    WEAPON = 'WP', 'Weapon'
    VESSEL = 'VS', 'Vessel'
    OTHER = 'OT', 'Other'

class GlassArtifactType(models.TextChoices):
    VESSEL = 'VS', 'Vessel'
    BEAD = 'BD', 'Bead'
    WINDOW = 'WN', 'Window'
    FRAGMENT = 'FR', 'Fragment'
    OTHER = 'OT', 'Other'


# ORGANICS DROPDOWNS
class AnimalFamily(models.TextChoices):
    BOVIDAE = 'BV', 'Bovidae (Cattle, Sheep, Goats)'
    CERVIDAE = 'CV', 'Cervidae (Deer)'
    EQUIDAE = 'EQ', 'Equidae (Horse family)'
    CANIDAE = 'CN', 'Canidae (Dogs, Wolves)'
    HOMINIDAE = 'HM', 'Hominidae (Humans)'
    AVES = 'AV', 'Aves (Birds)'
    OTHER = 'OT', 'Other'

class ElementType(models.TextChoices):
    CRANIUM = 'CR', 'Cranium'
    TOOTH = 'TH', 'Tooth'
    VERTEBRA = 'VT', 'Vertebra'
    LIMB = 'LM', 'Limb bone'
    PELVIS = 'PL', 'Pelvis'
    OTHER = 'OT', 'Other'

class SideType(models.TextChoices):
    LEFT = 'L', 'Left'
    RIGHT = 'R', 'Right'
    AXIAL = 'A', 'Axial'
    UNKNOWN = 'U', 'Unknown'

class PortionType(models.TextChoices):
    COMPLETE = 'CM', 'Complete'
    FRAGMENT = 'FR', 'Fragment'
    
class AgeType(models.TextChoices):
    JUVENILE = 'JV', 'Juvenile'
    ADULT = 'AD', 'Adult'
    UNKNOWN = 'UN', 'Unknown'

class SexType(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    INDETERMINATE = 'I', 'Indeterminate'

class SizeType(models.TextChoices):
    SMALL = 'SM', 'Small'
    MEDIUM = 'MD', 'Medium'
    LARGE = 'LG', 'Large'

class ModificationType(models.TextChoices):
    NONE = 'NO', 'None'
    CUT = 'CT', 'Cut Marks'
    BURNED = 'BR', 'Burned'
    WORKED = 'WK', 'Worked'
    OTHER = 'OT', 'Other'

class WorkedBoneType(models.TextChoices):
    TOOL = 'TL', 'Tool'
    ORNAMENT = 'OR', 'Ornament'
    OTHER = 'OT', 'Other'
    

# DOCUMENTATION DROPDOWNS
class LoanStatusType(models.TextChoices):
    ACTIVE = 'AC', 'Active'
    RETURNED = 'RT', 'Returned'
    OVERDUE = 'OD', 'Overdue'
    DAMAGED = 'DM', 'ReturnedDamaged'
    LOST = 'LT', 'Lost'


# PROVINENCE MODEL CLASSES
class Sites(models.Model):
    siteNo = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    longitude = models.DecimalField(max_digits=7, decimal_places=4, null=True, blank=True)
    length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    type = models.CharField(
        max_length=2,
        choices=SiteType.choices,
        null=True, 
        blank=True
    )
    terrain = models.CharField(
        max_length=2,
        choices=TerrainType.choices,
        null=True,
        blank=True
    )
    condition = models.CharField(
        max_length=2,
        choices=ConditionType.choices,
        null=True,
        blank=True
    )
    stratification = models.CharField(max_length=50, null=True, blank=True)
    surfaceVisibility = models.CharField(
        max_length=2,
        choices=VisibilityType.choices,
        null=True,
        blank=True
    )
    elevation = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"{self.siteNo}"
    
class Areas(models.Model):
    siteNo = models.ForeignKey(Sites, on_delete=models.CASCADE)
    areaNo = models.CharField(max_length=20, primary_key=True)
    
    def __str__(self):
        return f"{self.siteNo} - Area {self.areaNo}"

class Loci(models.Model):
    siteNo = models.ForeignKey(Sites, on_delete=models.CASCADE)
    areaNo = models.ForeignKey(Areas, on_delete=models.CASCADE)
    locus = models.CharField(max_length=20, primary_key=True)
    type = models.CharField(
        max_length=2,
        choices=LociType.choices
    )
    colour = models.CharField(max_length=50)  # hue/value/chroma
    inclusions = models.CharField(
        max_length=2,
        choices=InclusionType.choices
    )
    compaction = models.CharField(max_length=50)
    roundness = models.CharField(
        max_length=2,
        choices=RoundnessType.choices
    )
    density = models.CharField(
        max_length=2,
        choices=DensityType.choices
    )
    texture = models.CharField(
        max_length=4,
        choices=TextureType.choices
    )
    excavatedVolume = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    comments = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.siteNo} - Area {self.areaNo} - Locus {self.locus}"
    
    class Meta:
        verbose_name_plural = "Loci"

class Bags(models.Model):
    siteNo = models.ForeignKey(Sites, on_delete=models.CASCADE)
    areaNo = models.ForeignKey(Areas, on_delete=models.CASCADE)
    bagNo = models.CharField(max_length=20, primary_key=True)
    
    def __str__(self):
        return f"{self.siteNo} - Area {self.areaNo} - Bag {self.bagNo}"
    
    class Meta:
        verbose_name_plural = "Bags"

class Artifacts(models.Model):
    siteNo = models.ForeignKey(Sites, on_delete=models.CASCADE)
    areaNo = models.ForeignKey(Areas, on_delete=models.CASCADE)
    bagNo = models.ForeignKey(Bags, on_delete=models.CASCADE)
    artifactNo = models.CharField(max_length=20, primary_key=True)
    
    def __str__(self):
        return f"{self.siteNo} - Area {self.areaNo} - Bag {self.bagNo} - Artifact {self.artifactNo}"
    
    class Meta:
        verbose_name_plural = "Artifacts"


# CERAMICS MODEL CLASSES
class Pottery_Main(models.Model):
    siteNo = models.ForeignKey(Sites, on_delete=models.CASCADE)
    areaNo = models.ForeignKey(Areas, on_delete=models.CASCADE)
    bagNo = models.ForeignKey(Bags, on_delete=models.CASCADE)
    artifactNo = models.OneToOneField(Artifacts, on_delete=models.CASCADE, primary_key=True)
    type = models.CharField(
        max_length=2,
        choices=PotteryType.choices
    )
    length = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    mass = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.artifactNo} - {self.get_type_display()}"
    
    class Meta:
        verbose_name_plural = "Pottery Main"
        
class Pottery_Rims(models.Model):
    siteNo = models.ForeignKey(Sites, on_delete=models.CASCADE)
    areaNo = models.ForeignKey(Areas, on_delete=models.CASCADE)
    bagNo = models.ForeignKey(Bags, on_delete=models.CASCADE)
    artifactNo = models.OneToOneField(Artifacts, on_delete=models.CASCADE, primary_key=True)
    rimForm = models.CharField(
        max_length=2,
        choices=RimFormType.choices,
        null=True,
        blank=True
    )
    rimStance = models.CharField(
        max_length=2,
        choices=RimStanceType.choices,
        null=True,
        blank=True
    )
    rimProfile = models.CharField(
        max_length=2,
        choices=RimProfileType.choices,
        null=True,
        blank=True
    )
    rimLipShape = models.CharField(
        max_length=2,
        choices=LipShapeType.choices,
        null=True,
        blank=True
    )
    rimLipSymmetry = models.CharField(
        max_length=2,
        choices=SymmetryType.choices,
        null=True,
        blank=True
    )
    outsideRimDiameter = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    insideRimDiameter = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    rimHeight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    rimThickness = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    neckHeight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    neckDiameter = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    rimPercentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.artifactNo} - Rim"
    
    class Meta:
        verbose_name_plural = "Pottery Rims"
        
class Pottery_Bases(models.Model):
    siteNo = models.ForeignKey(Sites, on_delete=models.CASCADE)
    areaNo = models.ForeignKey(Areas, on_delete=models.CASCADE)
    bagNo = models.ForeignKey(Bags, on_delete=models.CASCADE)
    artifactNo = models.OneToOneField(Artifacts, on_delete=models.CASCADE, primary_key=True)
    baseForm = models.CharField(
        max_length=2,
        choices=BaseFormType.choices,
        null=True,
        blank=True
    )
    baseStance = models.CharField(
        max_length=2,
        choices=BaseStanceType.choices,
        null=True,
        blank=True
    )
    baseProfile = models.CharField(
        max_length=2,
        choices=BaseProfileType.choices,
        null=True,
        blank=True
    )
    baseJunction = models.CharField(
        max_length=2,
        choices=BaseJunctionType.choices,
        null=True,
        blank=True
    )
    outsideBaseDiameter = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    insideBaseDiameter = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    baseHeight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    baseThickness = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    basePercentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.artifactNo} - Base"
    
    class Meta:
        verbose_name_plural = "Pottery Bases"
        
class Pottery_Handles(models.Model):
    siteNo = models.ForeignKey(Sites, on_delete=models.CASCADE)
    areaNo = models.ForeignKey(Areas, on_delete=models.CASCADE)
    bagNo = models.ForeignKey(Bags, on_delete=models.CASCADE)
    artifactNo = models.OneToOneField(Artifacts, on_delete=models.CASCADE, primary_key=True)
    handleType = models.CharField(
        max_length=2,
        choices=HandleTypeType.choices,
        null=True,
        blank=True
    )
    handleSection = models.CharField(
        max_length=2,
        choices=HandleSectionType.choices,
        null=True,
        blank=True
    )
    handleAttachment = models.CharField(
        max_length=2,
        choices=HandleAttachmentType.choices,
        null=True,
        blank=True
    )
    handleLength = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    handleWidth = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    handleThickness = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.artifactNo} - Handle"
    
    class Meta:
        verbose_name_plural = "Pottery Handles"



# LITHICS MODEL CLASSES
class Cores(models.Model):
    siteNo = models.ForeignKey(Sites, on_delete=models.CASCADE)
    areaNo = models.ForeignKey(Areas, on_delete=models.CASCADE)
    bagNo = models.ForeignKey(Bags, on_delete=models.CASCADE)
    artifactNo = models.OneToOneField(Artifacts, on_delete=models.CASCADE, primary_key=True)
    coreCode = models.CharField(
        max_length=2,
        choices=CoreCodeType.choices,
        null=True,
        blank=True
    )
    coreType = models.CharField(
        max_length=2,
        choices=CoreType.choices,
        null=True,
        blank=True
    )
    platformLength = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    platformWidth = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    platformHeight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    platformCode = models.CharField(
        max_length=2,
        choices=PlatformCodeType.choices,
        null=True, 
        blank=True
    )
    platformType = models.CharField(
        max_length=2,
        choices=PlatformType.choices,
        null=True,
        blank=True
    )
    platformPrep = models.CharField(
        max_length=2,
        choices=PlatformPrepType.choices,
        null=True,
        blank=True
    )
    numVisibleFlakes = models.PositiveIntegerField(null=True, blank=True)
    stageOfUse = models.CharField(
        max_length=2,
        choices=StageOfUseType.choices,
        null=True,
        blank=True
    )
    rawMaterial = models.CharField(
        max_length=2,
        choices=RawMaterialType.choices,
        null=True,
        blank=True
    )
    geologicalCondition = models.CharField(
        max_length=2,
        choices=GeologicalConditionType.choices,
        null=True,
        blank=True
    )
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    photos = models.FileField(upload_to='lithics/cores/photos/', null=True, blank=True)
    drawings = models.FileField(upload_to='lithics/cores/drawings/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.artifactNo} - Core ({self.get_coreType_display() if self.coreType else 'Unclassified'})"
    
    class Meta:
        verbose_name_plural = "Cores"

class BladeFlake_Tool(models.Model):
    siteNo = models.ForeignKey(Sites, on_delete=models.CASCADE)
    areaNo = models.ForeignKey(Areas, on_delete=models.CASCADE)
    bagNo = models.ForeignKey(Bags, on_delete=models.CASCADE)
    artifactNo = models.OneToOneField(Artifacts, on_delete=models.CASCADE, primary_key=True)
    bladeCode = models.CharField(
        max_length=2,
        choices=BladeCodeType.choices,
        null=True,
        blank=True
    )
    toolType = models.CharField(
        max_length=2,
        choices=ToolTypeType.choices,
        null=True,
        blank=True
    )
    maxLength = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    maxWidth = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    hardHammer = models.CharField(
        max_length=1,
        choices=HammerType.choices,
        null=True,
        blank=True
    )
    backingCode = models.CharField(
        max_length=2,
        choices=BackingCodeType.choices,
        null=True,
        blank=True
    )
    backingType = models.CharField(
        max_length=2,
        choices=BackingTypeType.choices,
        null=True,
        blank=True
    )
    retouchCode = models.CharField(
        max_length=2,
        choices=RetouchCodeType.choices,
        null=True,
        blank=True
    )
    retouchType = models.CharField(
        max_length=2,
        choices=RetouchTypeType.choices,
        null=True,
        blank=True
    )
    percentageOfT = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    rawMaterial = models.CharField(
        max_length=2,
        choices=RawMaterialType.choices,
        null=True,
        blank=True
    )
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    useWearResult = models.CharField(
        max_length=2,
        choices=UseWearResultType.choices,
        null=True,
        blank=True
    )
    photos = models.FileField(upload_to='lithics/tools/photos/', null=True, blank=True)
    drawings = models.FileField(upload_to='lithics/tools/drawings/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.artifactNo} - {self.get_toolType_display() if self.toolType else 'Tool'}"
    
    class Meta:
        verbose_name_plural = "Blade/Flake Tools"

class Debitage(models.Model):
    siteNo = models.ForeignKey(Sites, on_delete=models.CASCADE)
    areaNo = models.ForeignKey(Areas, on_delete=models.CASCADE)
    bagNo = models.ForeignKey(Bags, on_delete=models.CASCADE)
    artifactNo = models.OneToOneField(Artifacts, on_delete=models.CASCADE, primary_key=True)
    debitageCode = models.CharField(
        max_length=2,
        choices=DebitageCodeType.choices,
        null=True,
        blank=True
    )
    debitageType = models.CharField(
        max_length=2,
        choices=DebitageTypeType.choices,
        null=True,
        blank=True
    )
    maxLength = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    maxWidth = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    hardHammer = models.CharField(
        max_length=1,
        choices=HammerType.choices,
        null=True,
        blank=True
    )
    softHammer = models.CharField(
        max_length=1,
        choices=HammerType.choices,
        null=True,
        blank=True
    )
    indirectPercussion = models.CharField(
        max_length=1,
        choices=HammerType.choices,
        null=True,
        blank=True
    )
    geologicalCondition = models.CharField(
        max_length=2,
        choices=GeologicalConditionType.choices,
        null=True,
        blank=True
    )
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    rawMaterial = models.CharField(
        max_length=2,
        choices=RawMaterialType.choices,
        null=True,
        blank=True
    )
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.artifactNo} - {self.get_debitageCode_display() if self.debitageCode else 'Debitage'}"
    
    class Meta:
        verbose_name_plural = "Debitage"


# METALS MODEL CLASSES
class Metal_Objects(models.Model):
    siteNo = models.ForeignKey(Sites, on_delete=models.CASCADE)
    areaNo = models.ForeignKey(Areas, on_delete=models.CASCADE)
    bagNo = models.ForeignKey(Bags, on_delete=models.CASCADE)
    artifactNo = models.OneToOneField(Artifacts, on_delete=models.CASCADE, primary_key=True)
    mcNo = models.CharField(max_length=30, null=True, blank=True)  # Material Culture Number
    artifactType = models.CharField(
        max_length=2,
        choices=MetalArtifactType.choices,
        null=True,
        blank=True
    )
    metal = models.CharField(
        max_length=2,
        choices=MetalType.choices,
        null=True,
        blank=True
    )
    comments = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.artifactNo} - {self.get_artifactType_display() if self.artifactType else 'Metal Object'}"
    
    class Meta:
        verbose_name_plural = "Metal Objects"

class Glass(models.Model):
    siteNo = models.ForeignKey(Sites, on_delete=models.CASCADE)
    areaNo = models.ForeignKey(Areas, on_delete=models.CASCADE)
    bagNo = models.ForeignKey(Bags, on_delete=models.CASCADE)
    artifactNo = models.OneToOneField(Artifacts, on_delete=models.CASCADE, primary_key=True)
    mcNo = models.CharField(max_length=30, null=True, blank=True)  # Material Culture Number
    artifactType = models.CharField(
        max_length=2,
        choices=GlassArtifactType.choices,
        null=True,
        blank=True
    )
    comments = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.artifactNo} - {self.get_artifactType_display() if self.artifactType else 'Glass'}"
    
    class Meta:
        verbose_name_plural = "Glass"

class Special_Finds(models.Model):
    siteNo = models.ForeignKey(Sites, on_delete=models.CASCADE)
    areaNo = models.ForeignKey(Areas, on_delete=models.CASCADE)
    bagNo = models.ForeignKey(Bags, on_delete=models.CASCADE)
    artifactNo = models.OneToOneField(Artifacts, on_delete=models.CASCADE, primary_key=True)
    mcNo = models.CharField(max_length=30, null=True, blank=True)  # Material Culture Number
    description = models.TextField()
    comments = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.artifactNo} - Special Find"
    
    class Meta:
        verbose_name_plural = "Special Finds"


# ORGANICS MODEL CLASSES
class Osteology(models.Model):
    siteNo = models.ForeignKey(Sites, on_delete=models.CASCADE)
    areaNo = models.ForeignKey(Areas, on_delete=models.CASCADE)
    bagNo = models.ForeignKey(Bags, on_delete=models.CASCADE)
    artifactNo = models.OneToOneField(Artifacts, on_delete=models.CASCADE, primary_key=True)
    family = models.CharField(
        max_length=2,
        choices=AnimalFamily.choices,
        null=True,
        blank=True
    )
    genus = models.CharField(max_length=50, null=True, blank=True)
    species = models.CharField(max_length=50, null=True, blank=True)
    element = models.CharField(
        max_length=2,
        choices=ElementType.choices,
        null=True,
        blank=True
    )
    side = models.CharField(
        max_length=1,
        choices=SideType.choices,
        null=True,
        blank=True
    )
    portion = models.CharField(
        max_length=2,
        choices=PortionType.choices,
        null=True,
        blank=True
    )
    percentComplete = models.PositiveIntegerField(null=True, blank=True)
    age = models.CharField(
        max_length=2,
        choices=AgeType.choices,
        null=True,
        blank=True
    )
    sex = models.CharField(
        max_length=1,
        choices=SexType.choices,
        null=True,
        blank=True
    )
    size = models.CharField(
        max_length=2,
        choices=SizeType.choices,
        null=True,
        blank=True
    )
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    modification = models.CharField(
        max_length=2,
        choices=ModificationType.choices,
        null=True,
        blank=True
    )
    comments = models.TextField(blank=True)
    order = models.PositiveIntegerField(null=True, blank=True)  # Taxonomic order
    
    def __str__(self):
        if self.genus and self.species:
            species_name = f"{self.genus} {self.species}"
        else:
            species_name = self.get_family_display() if self.family else "Unidentified"
        
        element_name = self.get_element_display() if self.element else "bone"
        return f"{self.artifactNo} - {species_name} {element_name}"
    
    class Meta:
        verbose_name_plural = "Osteology"

class Worked_Bone(models.Model):
    siteNo = models.ForeignKey(Sites, on_delete=models.CASCADE)
    areaNo = models.ForeignKey(Areas, on_delete=models.CASCADE)
    bagNo = models.ForeignKey(Bags, on_delete=models.CASCADE)
    artifactNo = models.OneToOneField(Artifacts, on_delete=models.CASCADE, primary_key=True)
    artifactType = models.CharField(
        max_length=2,
        choices=WorkedBoneType.choices,
        null=True,
        blank=True
    )
    mcNo = models.CharField(max_length=30, null=True, blank=True)  # Material Culture Number
    comments = models.TextField(blank=True)
    related_osteology = models.ForeignKey(Osteology, on_delete=models.SET_NULL, null=True, blank=True, related_name='worked_bone')
    
    def __str__(self):
        return f"{self.artifactNo} - {self.get_artifactType_display() if self.artifactType else 'Worked Bone'}"
    
    class Meta:
        verbose_name_plural = "Worked Bone"


# DOCUMENTATION MODEL CLASSES
class Photos(models.Model):
    siteNo = models.ForeignKey(Sites, on_delete=models.CASCADE)
    photoNo = models.CharField(max_length=20, primary_key=True)
    date = models.DateField()
    photo = models.ImageField(upload_to='photos/')
    photographer = models.CharField(max_length=100)
    caption = models.TextField()
    
    def __str__(self):
        return f"{self.siteNo} - Photo {self.photoNo}"
    
    class Meta:
        verbose_name_plural = "Photos"

class Loans(models.Model):
    siteNo = models.ForeignKey(Sites, on_delete=models.CASCADE)
    areaNo = models.ForeignKey(Areas, on_delete=models.CASCADE)
    bagNo = models.ForeignKey(Bags, on_delete=models.CASCADE)
    artifactNo = models.ForeignKey(Artifacts, on_delete=models.CASCADE)
    loanee = models.CharField(max_length=100)
    status = models.CharField(
        max_length=2,
        choices=LoanStatusType.choices,
        default=LoanStatusType.ACTIVE
    )
    dateLoaned = models.DateField()
    
    class Meta:
        unique_together = ['artifactNo', 'loanee', 'dateLoaned']
        verbose_name_plural = "Loans"
    
    def __str__(self):
        return f"{self.artifactNo} loaned to {self.loanee} on {self.dateLoaned}"