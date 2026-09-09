import uuid
from django.db import models
from django.core.exceptions import ValidationError

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

