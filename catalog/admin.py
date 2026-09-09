from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Category,
    CoolFont,
    DiyEffect,
    DiyFont,
    DiyImage,
    DiyKey,
    DiySound,
    Keyboard,
    SubCategory,
    Theme,
    ThemeIcon,
    Wallpaper,
)

# Register your models here.

class ImagePreviewMixin:
    @admin.display(description="Preview")
    def image_preview(self, obj):
        possible_fields = (
            "thumbnail",
            "preview_url",
            "image_url",
            "keyboard_bg",
            "icon_image",
            "gif_url",
        )

        for field_name in possible_fields:
            url = getattr(obj, field_name, "")
            if url:
                return format_html(
                    '<img src="{}" '
                    'style="width: 48px; height: 48px; '
                    'object-fit: cover; border-radius: 4px;">',
                    url,
                )
        return "-"


@admin.register(Category)
class CategoryAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "type",
        "image_preview",
        "priority",
    )
    list_filter = ("type",)
    search_fields = ("name",)
    list_editable = ("priority",)
    readonly_fields = ("id",)
    ordering = ("priority", "name")


@admin.register(SubCategory)
class SubCategoryAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "image_preview",
        "priority",
    )
    list_filter = ("category",)
    search_fields = ("name", "category__name")
    list_editable = ("priority",)
    readonly_fields = ("id",)
    autocomplete_fields = ("category",)
    ordering = ("priority", "name")


class CatalogItemAdmin(ImagePreviewMixin, admin.ModelAdmin):
    expected_category_type = None

    list_display = (
        "name",
        "category",
        "subcategory",
        "image_preview",
        "premium",
        "priority",
        "created_at",
    )
    list_filter = ("premium", "category")
    search_fields = (
        "name",
        "category__name",
        "subcategory__name",
    )
    list_editable = ("premium", "priority")
    readonly_fields = ("id", "created_at")
    ordering = ("priority", "-created_at")

    def formfield_for_foreignkey(
        self,
        db_field,
        request,
        **kwargs,
    ):
        if self.expected_category_type:
            if db_field.name == "category":
                kwargs["queryset"] = Category.objects.filter(
                    type=self.expected_category_type,
                )

            elif db_field.name == "subcategory":
                kwargs["queryset"] = SubCategory.objects.filter(
                    category__type=self.expected_category_type,
                )

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs,
        )


@admin.register(CoolFont)
class CoolFontAdmin(CatalogItemAdmin):
    expected_category_type = Category.Type.COOL_FONT


@admin.register(Keyboard)
class KeyboardAdmin(CatalogItemAdmin):
    expected_category_type = Category.Type.KEYBOARD


@admin.register(Wallpaper)
class WallpaperAdmin(CatalogItemAdmin):
    expected_category_type = Category.Type.WALLPAPER


class ThemeIconInline(admin.TabularInline):
    model = ThemeIcon
    extra = 0
    fields = (
        "name",
        "preview_url",
        "icon_image",
        "alias_id",
        "priority",
    )
    ordering = ("priority",)


@admin.register(Theme)
class ThemeAdmin(CatalogItemAdmin):
    expected_category_type = Category.Type.THEME
    inlines = (ThemeIconInline,)
    autocomplete_fields = ("keyboard", "wallpaper")


@admin.register(ThemeIcon)
class ThemeIconAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "theme",
        "alias_id",
        "image_preview",
        "priority",
        "created_at",
    )
    list_filter = ("theme",)
    search_fields = ("name", "alias_id", "theme__name")
    list_editable = ("priority",)
    readonly_fields = ("id", "created_at")
    autocomplete_fields = ("theme",)
    ordering = ("priority", "-created_at")


@admin.register(
    DiyImage,
    DiyKey,
    DiyFont,
    DiyEffect,
    DiySound,
)
class DiyAssetAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "image_preview",
        "priority",
        "created_at",
    )
    search_fields = ("name",)
    list_editable = ("priority",)
    readonly_fields = ("id", "created_at")
    ordering = ("priority", "-created_at")


admin.site.site_header = "Mobile Theme Administration"
admin.site.site_title = "Mobile Theme Admin"
admin.site.index_title = "Catalog Management"
