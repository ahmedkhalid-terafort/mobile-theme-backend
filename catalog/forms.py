from django import forms

from .models import Category, SubCategory, CoolFont, Keyboard, Wallpaper, Theme, ThemeIcon, DiyImage, DiyKey, DiyFont, DiyEffect, DiySound

class CategoryAdminForm(forms.ModelForm):
    thumbnail_upload = forms.FileField(
        required=False,
        label="Upload thumbnail",
    )

    class Meta:
        model = Category
        fields = "__all__"


class SubCategoryAdminForm(forms.ModelForm):
    thumbnail_upload = forms.FileField(
        required=False,
        label="Upload thumbail"
    )

    class Meta:
        model = SubCategory
        fields = "__all__"


class CoolFontAdminForm(forms.ModelForm):
    thumbnail_upload = forms.FileField(
        required=False,
        label="Upload thumbnail"
    )

    class Meta:
        model = CoolFont
        fields = "__all__"



class KeyboardAdminForm(forms.ModelForm):
    preview_upload = forms.FileField(
        required=False,
        label="Upload preview",
    )

    backspace_key_bg_upload = forms.FileField(
        required=False,
        label="Upload backspace key background"
    )

    uppercase_letter_bg_upload = forms.FileField(
        required=False,
        label="Upload uppercase letter background"
    )

    number_button_bg_upload = forms.FileField(
        required=False,
        label="Upload number button background"
    )

    emoji_button_bg_upload = forms.FileField(
        required=False,
        label="Upload emoji button background"
    )

    comma_button_bg_upload = forms.FileField(
        required=False,
        label="Upload comma button background"
    )

    enter_button_bg_upload = forms.FileField(
        required=False,
        label="Upload enter button background"
    )

    keyboard_bg_upload = forms.FileField(
        required=False,
        label="Upload keyboard background"
    )

    keyboard_bg = forms.URLField(
        required=False,
        label="Keyboard background URL",
    )

    normal_key_bg = forms.URLField(
        required=False,
        label="Normal key background URL"
    )

    normal_key_bg_upload = forms.FileField(
        required=False,
        label="Normal key background upload"
    )

    specialty_keys_bg = forms.URLField(
        required=False,
        label="Specialty key URL"
    )

    specialty_keys_bg_upload = forms.FileField(
        required=False,
        label="Specialty Key background upload"
    )

    class Meta:
        model = Keyboard
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        has_keyboard_bg_url = cleaned_data.get("keyboard_bg")
        has_keyboard_bg_upload = cleaned_data.get("keyboard_bg_upload")

        has_normal_key_url = cleaned_data.get("normal_key_bg")
        has_normal_key_upload = cleaned_data.get("normal_key_bg_upload")

        has_specialty_key_url = cleaned_data.get("specialty_keys_bg")
        has_specialty_key_upload = cleaned_data.get("specialty_keys_bg_upload")


        if not has_keyboard_bg_url and not has_keyboard_bg_upload:
            self.add_error(
                "keyboard_bg_upload",
                "Enter a URL or upload a file."
            )

        if not has_normal_key_url and not has_normal_key_upload:
            self.add_error(
                "normal_key_bg_upload",
                "Enter a URL or upload a file"
            )

        if not has_specialty_key_url and not has_specialty_key_upload:
            self.add_error(
                "specialty_keys_bg_upload",
                "Enter a URL or upload a file"
            )

        return cleaned_data


class WallpaperAdminForm(forms.ModelForm):
    preview_upload = forms.FileField(
        required=False,
        label="Upload preview"
    )

    image_upload = forms.FileField(
        required=False,
        label="Upload Image"
    )

    image_url = forms.URLField(
        required=False,
        label="Image URL"
    )

    class Meta:
        model = Wallpaper
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        has_image_upload = cleaned_data.get("image_upload")
        has_image_url = cleaned_data.get("image_url")

        if not has_image_upload and not has_image_url:
            self.add_error(
                "image_upload",
                "Upload an image"
            )

        return cleaned_data


class ThemeAdminForm(forms.ModelForm):
    preview_upload = forms.FileField(
        required=False,
        label="Upload preview"
    )

    class Meta:
        model = Theme
        fields = "__all__"


class ThemeIconAdminForm(forms.ModelForm):
    preview_upload = forms.FileField(
        required=False,
        label="Upload preview"
    )

    icon_image = forms.URLField(
        required=False,
        label="Enter icon URL"
    )

    icon_upload = forms.FileField(
        required=False,
        label="Upload Image"
    )


    class Meta:
        model = ThemeIcon
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
    
        has_icon_image = cleaned_data.get("icon_upload")
        has_icon_url = cleaned_data.get("icon_image")
    
        if not has_icon_image and not has_icon_url:
            self.add_error(
                "icon_upload",
                "Upload an icon"
            )
        return cleaned_data


class DiyImageAdminForm(forms.ModelForm):
    image_upload = forms.FileField(
        required=False,
        label="Upload Image"
    )

    image_url = forms.URLField(
        required=False,
        label="Image URL"
    )

    class Meta:
        model = DiyImage
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        has_image_upload = cleaned_data.get("image_upload")
        has_image_url = cleaned_data.get("image_url")

        if not has_image_upload and not has_image_url:
            self.add_error(
                "image_upload",
                "Upload an image"
            )
        return cleaned_data


class DiyKeyAdminForm(forms.ModelForm):
    image_upload = forms.FileField(
        required=False,
        label="Upload Image"
    )

    image_url = forms.URLField(
        required=False,
        label="Image URL"
    )

    special_key_upload = forms.FileField(
        required=False,
        label="Upload specialty key"
    )

    special_key_bg = forms.URLField(
        required=False,
        label="Specialty key background url"
    )

    class Meta:
        model = DiyKey
        fields = "__all__"

    def clean(self):
        cleaned_data =  super().clean()

        has_image_upload = cleaned_data.get("image_upload")
        has_image_url = cleaned_data.get("image_url")
        has_special_key_upload = cleaned_data.get("special_key_upload")
        has_special_key_url = cleaned_data.get("special_key_bg")

        if not has_image_upload and not has_image_url:
            self.add_error(
                "image_upload",
                "Upload an image"
            )
        if not has_special_key_upload and not has_special_key_url:
            self.add_error(
                "special_key_upload",
                "Upload a special key"
            )

        return cleaned_data


class DiyFontAdminForm(forms.ModelForm):
    font_upload = forms.FileField(
        required=False,
        label="Upload font"
    )

    font_url = forms.URLField(
        required=False,
        label="Font URL"
    )

    class Meta:
        model = DiyFont
        fields ="__all__"

    def clean(self):
        cleaned_data =  super().clean()

        has_font_upload = cleaned_data.get("font_upload")
        has_font_url = cleaned_data.get("font_url")

        if not has_font_upload and not has_font_url:
            self.add_error(
                "font_upload",
                "Upload a font"
            )

        return cleaned_data


class DiyEffectAdminForm(forms.ModelForm):
    gif_upload = forms.FileField(
        required=False,
        label="Upload gif"
    )

    gif_url = forms.URLField(
        required=False,
        label="GIF URL"
    )

    preview_upload = forms.FileField(
        required=False,
        label="Upload preview"
    )


    class Meta:
        model = DiyEffect
        fields = "__all__"

    def clean(self):
        cleaned_data =  super().clean()

        has_gif_upload = cleaned_data.get("gif_upload")
        has_gif_url = cleaned_data.get("gif_url")

        if not has_gif_upload and not has_gif_url:
            self.add_error(
                "gif_upload",
                "Upload a GIF"
            )

        return cleaned_data



class DiySoundAdminForm(forms.ModelForm):
    sound_upload = forms.FileField(
        required=False,
        label="Upload sound"
    )

    sound_url = forms.URLField(
        required=False,
        label="Sound URL"
    )

    preview_upload = forms.FileField(
        required=False,
        label="Upload preview"
    )

    class Meta:
        model = DiySound
        fields = "__all__"

    def clean(self):
        cleaned_data =  super().clean()

        has_sound_upload = cleaned_data.get("sound_upload")
        has_sound_url = cleaned_data.get("sound_url")

        if not has_sound_upload and not has_sound_url:
            self.add_error(
                "sound_upload",
                "Upload a Diy sound"
            )

        return cleaned_data



