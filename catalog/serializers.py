from rest_framework import serializers

from .models import Category, CoolFont, SubCategory, Keyboard, Wallpaper, Theme, ThemeIcon, DiyImage, DiyFont, DiyEffect, DiyKey, DiySound


class CategorySerializer(serializers.ModelSerializer):
    has_subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "type",
            "thumbnail",
            "priority",
            "has_subcategories",
        )

    def  get_has_subcategories(self, obj):
        return obj.subcategories.exists()



class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = (
            "id",
            "name",
            "thumbnail",
            "priority",
        )



class CoolFontSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    subcategory_name = serializers.CharField(
        source = "subcategory.name",
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = CoolFont
        fields = (
            "id",
            "name",
            "category_id",
            "category_name",
            "subcategory_id",
            "subcategory_name",
            "content",
            "thumbnail",
            "premium",
            "priority",
            "created_at",
        )




class KeyboardSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    subcategory_name = serializers.CharField(
        source="subcategory.name",
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Keyboard
        fields = (
            "id",
            "name",
            "category_id",
            "category_name",
            "subcategory_id",
            "subcategory_name",
            "premium",
            "preview_url",
            "text_color",
            "key_alpha",
            "keyboard_bg",
            "normal_key_bg",
            "specialty_keys_bg",
            "backspace_key_bg",
            "uppercase_letter_bg",
            "number_button_bg",
            "emoji_button_bg",
            "comma_button_bg",
            "enter_button_bg",
            "priority",
            "created_at"
        )


class WallpaperSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    subcategory_name = serializers.CharField(
        source="subcategory.name",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = Wallpaper
        fields = (
            "id",
            "name",
            "category_id",
            "category_name",
            "subcategory_id",
            "subcategory_name",
            "premium",
            "preview_url",
            "image_url",
            "priority",
            "created_at",
        )


class ThemeKeyboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyboard
        fields = (
            "id",
            "name",
            "preview_url",
            "text_color",
            "key_alpha",
            "keyboard_bg",
            "normal_key_bg",
            "specialty_keys_bg",
        )


class ThemeWallpaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallpaper
        fields = (
            "id",
            "name",
            "preview_url",
            "image_url",
        )


class ThemeIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeIcon
        fields = (
            "id",
            "name",
            "preview_url",
            "icon_image",
            "alias_id",
            "priority",
            "created_at",
        )


class ThemeSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    subcategory_name = serializers.CharField(
        source="subcategory.name",
        read_only=True,
        allow_null=True,
    )

    keyboard = ThemeKeyboardSerializer(read_only=True)
    wallpaper = ThemeWallpaperSerializer(read_only=True)
    icons = ThemeIconSerializer(many=True, read_only=True)

    class Meta:
        model = Theme
        fields = (
            "id",
            "name",
            "category_id",
            "category_name",
            "subcategory_id",
            "subcategory_name",
            "premium",
            "preview_url",
            "keyboard_id",
            "wallpaper_id",
            "keyboard",
            "wallpaper",
            "icons",
            "priority",
            "created_at",
        )


class DiyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiyImage
        fields = (
                "id",
                "name",
                "image_url",
                "description",
                "transparency",
                "priority",
                "created_at"
            )



class DiyFontSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = DiyFont
        fields = (
            "id",
            "name",
            "font_url",
            "priority",
            "created_at"
        )


class DiyEffectSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiyEffect
        fields = (
            "id",
            "name",
            "gif_url",
            "preview_url",
            "priority",
            "created_at"
        )


class DiyKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiyKey
        fields = (
            "id",
            "name",
            "image_url",
            "description",
            "transparency",
            "special_key_bg",
            "priority",
            "created_at"
        )


class DiySoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiySound
        fields = (
            "id",
            "name",
            "sound_url",
            "preview_url",
            "priority",
            "created_at"
        )
