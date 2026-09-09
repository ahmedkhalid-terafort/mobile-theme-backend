import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)

# Create your models here.

class UUIDModel(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    class Meta:
        abstract = True



class Category(UUIDModel):
    class Type(models.TextChoices):
        COOL_FONT = "coolfont", "Cool Font"
        KEYBOARD = "keyboard", "Keyboard"
        THEME = "theme", "Theme"
        WALLPAPER = "wallpaper", "Wallpaper"

    name = models.CharField(max_length=128)
    type = models.CharField(max_length=16, choices=Type.choices) 
    thumbnail = models.URLField(blank=True)
    priority = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ("priority", "name")

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"




class SubCategory(UUIDModel):
    name = models.CharField(max_length=128)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
    )
    thumbnail = models.URLField(blank=True)
    priority = models.IntegerField(default=0)

    class Meta:
        verbose_name = "sub category"
        verbose_name_plural = "sub categories"
        ordering = ("priority", "name")

    def __str__(self):
        return f"{self.category.name} / {self.name}"



class CatalogItem(UUIDModel):
    EXPECTED_CATEGORY_TYPE = None
    name  = models.CharField(max_length=256)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="%(class)s_items"
    )

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name="%(class)s_items",
        null=True,
        blank=True
    )

    premium = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ("priority", "-created_at")

    def clean(self):
        super().clean()

        errors = {}

        if(
            self.category_id
            and self.EXPECTED_CATEGORY_TYPE
            and self.category.type != self.EXPECTED_CATEGORY_TYPE
        ):
            expected_label = Category.Type(self.EXPECTED_CATEGORY_TYPE).label

            errors["category"] = (f"This item requires a {expected_label} category.")


        if (
            self.subcategory_id
            and self.subcategory.category_id != self.category_id
        ):
            errors["subcategory"] = ("The subcategory must belong to the selected category.")

        if errors:
            raise ValidationError(errors)


    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)



class CoolFont(CatalogItem):
    EXPECTED_CATEGORY_TYPE = Category.Type.COOL_FONT
    content = models.TextField()
    thumbnail = models.URLField(blank=True)

    class Meta(CatalogItem.Meta):
        verbose_name = "cool font"
        verbose_name_plural = "cool fonts"

    def __str__(self):
        return self.name



class Keyboard(CatalogItem):
    EXPECTED_CATEGORY_TYPE = Category.Type.KEYBOARD

    preview_url = models.URLField(blank=True)

    text_color = models.CharField(
        max_length=9,
        default="#FFFFFFFF",
        validators=[
            RegexValidator(
                regex=r"^#[0-9A-Fa-f]{8}$",
                message=(
                    "Enter a color using # followed by "
                    "eight hexadecimal characters."
                ),
            ),
        ],
    )
    key_alpha = models.FloatField(
        default=0.85,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(1.0),
        ],
    )

    keyboard_bg = models.URLField()
    normal_key_bg = models.URLField()
    specialty_keys_bg = models.URLField()

    backspace_key_bg = models.URLField(blank=True)
    uppercase_letter_bg = models.URLField(blank=True)
    number_button_bg = models.URLField(blank=True)
    emoji_button_bg = models.URLField(blank=True)
    comma_button_bg = models.URLField(blank=True)
    enter_button_bg = models.URLField(blank=True)

    class Meta(CatalogItem.Meta):
        verbose_name = "keyboard"
        verbose_name_plural = "keyboards"

    def __str__(self):
        return self.name



class Wallpaper(CatalogItem):
    EXPECTED_CATEGORY_TYPE = Category.Type.WALLPAPER

    preview_url = models.URLField(blank=True)
    image_url = models.URLField()

    class Meta(CatalogItem.Meta):
        verbose_name = "wallpaper"
        verbose_name_plural = "wallpapers"

    def __str__(self):
        return self.name


class Theme(CatalogItem):
    EXPECTED_CATEGORY_TYPE = Category.Type.THEME

    preview_url = models.URLField(blank=True)

    keyboard = models.ForeignKey(
        Keyboard,
        on_delete=models.SET_NULL,
        related_name="themes",
        null=True,
        blank=True,
    )

    wallpaper = models.ForeignKey(
        Wallpaper,
        on_delete=models.SET_NULL,
        related_name="themes",
        null=True,
        blank=True,
    )

    class Meta(CatalogItem.Meta):
        verbose_name = "theme"
        verbose_name_plural = "themes"

    def __str__(self):
        return self.name



class ThemeIcon(UUIDModel):
    theme = models.ForeignKey(
        Theme,
        on_delete=models.CASCADE,
        related_name="icons",
    )
    name = models.CharField(max_length=256)
    preview_url = models.URLField(blank=True)
    icon_image = models.URLField()
    alias_id = models.CharField(max_length=255)
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "theme icon"
        verbose_name_plural = "theme icons"
        ordering = ("priority", "-created_at")

    def __str__(self):
        return f"{self.theme.name} / {self.name}"



class DiyAsset(UUIDModel):
    """Common fields for independent DIY catalog assets."""

    name = models.CharField(max_length=256)
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ("priority", "-created_at")

    def __str__(self):
        return self.name



class DiyImage(DiyAsset):
    image_url = models.URLField()
    description = models.TextField(blank=True)
    transparency = models.FloatField(
        default=0.85,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(1.0),
        ],
    )



class DiyKey(DiyAsset):
    image_url = models.URLField()
    description = models.TextField(blank=True)
    transparency = models.FloatField(
        default=0.9,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(1.0),
        ],
    )
    special_key_bg = models.URLField()



class DiyFont(DiyAsset):
    font_url = models.URLField()



class DiyEffect(DiyAsset):
    gif_url = models.URLField()
    preview_url = models.URLField(blank=True)



class DiySound(DiyAsset):
    sound_url = models.URLField()
    preview_url = models.URLField(blank=True)