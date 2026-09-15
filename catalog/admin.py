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

from .forms import (
    CategoryAdminForm,
    CoolFontAdminForm,
    DiyEffectAdminForm,
    DiyFontAdminForm,
    DiyImageAdminForm,
    DiyKeyAdminForm,
    DiySoundAdminForm,
    KeyboardAdminForm,
    SubCategoryAdminForm,
    ThemeAdminForm,
    ThemeIconAdminForm,
    WallpaperAdminForm,
)
from .services.storage import upload_public_file

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


class StorageUploadAdminMixin:
    upload_fields = {}

    def save_model(self, request, obj, form, change):
        for upload_field_name, config in (self.upload_fields.items()):
            upload_file = form.cleaned_data.get(upload_field_name)

            if upload_file:
                public_url = upload_public_file(
                    upload_file,
                    config["folder"]
                )

                setattr(
                    obj, config["model_field"], public_url
                )

        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(StorageUploadAdminMixin ,ImagePreviewMixin, admin.ModelAdmin):
    form = CategoryAdminForm

    upload_fields = {
        "thumbnail_upload" :{
            "model_field": "thumbnail",
            "folder": "categories/thumbnails"
        },
    }

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
class SubCategoryAdmin(StorageUploadAdminMixin ,ImagePreviewMixin, admin.ModelAdmin):

    form = SubCategoryAdminForm
    upload_fields = {
        "thumbnail_upload": {
            "model_field": "thumbnail",
            "folder": "subcategories/thumbnails"
        }
    }
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


class CatalogItemAdmin(StorageUploadAdminMixin ,ImagePreviewMixin, admin.ModelAdmin):
    # expected_category_type = None

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

    # def formfield_for_foreignkey(
    #     self,
    #     db_field,
    #     request,
    #     **kwargs,
    # ):
    #     field_name = db_field.name
    #     category_type = self.expected_category_type

    #     if field_name == "category":
    #         valid_categories = Category.objects.filter(type=category_type)
    #         kwargs["queryset"] = valid_categories

    #     elif field_name == "subcategory":
    #         valid_subcategories = SubCategory.objects.filter(category__type=category_type)
    #         kwargs["queryset"] = valid_subcategories
            
    #     return super().formfield_for_foreignkey(
    #         db_field,
    #         request,
    #         **kwargs,
    #     )


@admin.register(CoolFont)
class CoolFontAdmin(CatalogItemAdmin):
    # expected_category_type = Category.Type.COOL_FONT

    form = CoolFontAdminForm

    upload_fields = {
        "thumbnail_upload": {
            "model_field": "thumbnail",
            "folder": "artwork/thumbnails"
        }
    }


@admin.register(Keyboard)
class KeyboardAdmin(CatalogItemAdmin):
    # expected_category_type = Category.Type.KEYBOARD

    form = KeyboardAdminForm

    upload_fields = {
        "preview_upload": {
            "model_field": "preview_url",
            "folder": "keyboards/previews"
        },
        "keyboard_bg_upload": {
            "model_field": "keyboard_bg",
            "folder": "keyboards/backgrounds"
        },
        "backspace_key_bg_upload" :{
            "model_field": "backspace_key_bg",
            "folder": "keyboards/backspace-keys"
        },
        "uppercase_letter_bg_upload": {
            "model_field": "uppercase_letter_bg",
            "folder": "keyboards/uppercase-keys"
        },
        "number_button_bg_upload": {
            "model_field": "number_button_bg",
            "folder": "keyboards/number-keys"
        },
        "emoji_button_bg_upload": {
            "model_field": "emoji_button_bg",
            "folder": "keyboards/emoji-keys"
        },
        "comma_button_bg_upload": {
            "model_field": "comma_button_bg",
            "folder": "keyboards/comma-keys"
        },
        "enter_button_bg_upload": {
            "model_field": "enter_button_bg",
            "folder": "keyboards/enter-keys"
        },
        "normal_key_bg_upload": {
            "model_field": "normal_key_bg",
            "folder": "keyboards/normal-keys"
        },
        "specialty_keys_bg_upload": {
            "model_field": "specialty_keys_bg",
            "folder": "keyboards/specialty-keys"
        }
    }


@admin.register(Wallpaper)
class WallpaperAdmin(CatalogItemAdmin):
    # expected_category_type = Category.Type.WALLPAPER

    form = WallpaperAdminForm

    upload_fields = {
        "preview_upload": {
            "model_field": "preview_url",
            "folder": "wallpapers/previews"
        },
        "image_upload": {
            "model_field": "image_url",
            "folder": "wallpapers/images"
        }
    }


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
    # expected_category_type = Category.Type.THEME
    form = ThemeAdminForm
    upload_fields = {
        "preview_upload": {
            "model_field": "preview_url",
            "folder": "themes/previews"
        }
    }
    inlines = (ThemeIconInline,)
    autocomplete_fields = ("keyboard", "wallpaper")


@admin.register(ThemeIcon)
class ThemeIconAdmin(StorageUploadAdminMixin ,ImagePreviewMixin, admin.ModelAdmin):

    form = ThemeIconAdminForm

    upload_fields = {
        "preview_upload": {
            "model_field": "preview_url",
            "folder": "themes/icons/previews",
        },
        "icon_upload": {
            "model_field": "icon_image",
            "folder": "themes/icons/images"
        }
    }
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



class DiyAssetAdmin(StorageUploadAdminMixin ,ImagePreviewMixin, admin.ModelAdmin):
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


@admin.register(DiyImage)
class DiyImageAdmin(DiyAssetAdmin):
    form = DiyImageAdminForm

    upload_fields = {
        "image_upload": {
            "model_field": "image_url",
            "folder": "diy/images"
        }
    }


@admin.register(DiyFont)
class DiyFontAdmin(DiyAssetAdmin):
    form = DiyFontAdminForm

    upload_fields = {
        "font_upload": {
            "model_field": "font_url",
            "folder": "diy/fonts",
        },
    }


@admin.register(DiyEffect)
class DiyEffectAdmin(DiyAssetAdmin):
    form = DiyEffectAdminForm

    upload_fields = {
        "gif_upload": {
            "model_field": "gif_url",
            "folder": "diy/effects/gifs",
        },
        "preview_upload": {
            "model_field": "preview_url",
            "folder": "diy/effects/previews",
        },
    }


@admin.register(DiyKey)
class DiyKeyAdmin(DiyAssetAdmin):
    form = DiyKeyAdminForm

    upload_fields = {
        "image_upload": {
            "model_field": "image_url",
            "folder": "diy/keys/images"
        },
        "special_key_upload": {
            "model_field": "special_key_bg",
            "folder": "diy/keys/special/diy-key"
        }
    }


@admin.register(DiySound)
class DiySoundAdmin(DiyAssetAdmin):
    form = DiySoundAdminForm

    upload_fields = {
        "sound_upload": {
            "model_field": "sound_url",
            "folder": "diy/sounds/files"
        },
        "preview_upload": {
            "model_field": "preview_url",
            "folder": "diy/sounds/previews"
        }
    }


admin.site.site_header = "Mobile Theme Administration"
admin.site.site_title = "Mobile Theme Admin"
admin.site.index_title = "Catalog Management"