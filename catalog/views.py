from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, CoolFont, Keyboard, Wallpaper, Theme, DiyImage, DiyFont, DiyEffect, DiyKey, DiySound
from .permissions import HasMobileThemeAPIKey
from .serializers import (
    CategorySerializer,
    CoolFontSerializer,
    SubCategorySerializer,
    KeyboardSerializer,
    DiyImageSerializer,
    DiyFontSerilaizer,
    DiyEffectSerializer,
    DiyKeySerializer,
    DiySoundSerializer
)

from .utils import get_pagination_params, apply_query_params_filters


class ArtworkCategoryListView(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request):
        categories = Category.objects.filter(
            type=Category.Type.COOL_FONT,
        )

        skip, limit, error_response = get_pagination_params(request=request, default_limit=100)
        if error_response is not None:
            return error_response

        # total = categories.count()
        total = len(categories)

        categories = categories[skip:skip + limit]

        serializer = CategorySerializer(
            categories,
            many=True,
        )

        return Response(
            {
                "status": 200,
                "data": {
                    "items": serializer.data,
                    "total": total,
                    "skip": skip,
                    "limit": limit
                },
                "message": "Artwork categories fetched successfully found.",
            },
            status=200,
        )



class ArtworkSubCategoryListView(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request, category_id):
        category = Category.objects.filter(
            id=category_id,
            type=Category.Type.COOL_FONT,
        ).first()

        if category is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "Artwork category not found.",
                },
                status=404
            )

        skip, limit, error_response = get_pagination_params(request=request, default_limit=100)

        if error_response is not None:
            return error_response

        subcategories = category.subcategories.all()
        # total = subcategories.count()
        total = len(subcategories)
        subcategories = subcategories[skip:skip + limit]

        serializer = SubCategorySerializer(
            subcategories,
            many = True
        )

        return Response(
            {
                "status": 200,
                "data": {
                    "items": serializer.data,
                    "total": total,
                    "skip": skip,
                    "limit": limit,
                },
                "message": "Artwork subcategories fetched successfully.",
            },
            status=200
        )



class ArtworkListView(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request):
        artworks = CoolFont.objects.select_related(
            "category",
            "subcategory"
        ).all()

        artworks, error_response = apply_query_params_filters(request=request, query_set=artworks)

        if error_response is not None:
            return error_response


        skip, limit, error_response = get_pagination_params(request=request, default_limit=20)

        if error_response is not None:
            return error_response

        # total = artworks.count()
        total = len(artworks)
        artworks = artworks[skip:skip + limit]

        serializer = CoolFontSerializer(
            artworks,
            many=True,
        )

        return Response(
            {
                "status": 200,
                "data": {
                    "items": serializer.data,
                    "total": total,
                    "skip": skip,
                    "limit": limit,
                },
                "message": "Artwork fetched successfully.",
            },
            status=200,
        )



class ArtworkDetailView(APIView):
    permission_classes = [HasMobileThemeAPIKey]

    def get(self, request, artwork_id):
        artwork = CoolFont.objects.select_related(
            "category",
            "subcategory",
        ).filter(id=artwork_id).first()

        if artwork is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "Artwork not found"
                },
                status=404
            )

        serializer = CoolFontSerializer(artwork)

        return Response(
            {
                "status": 200,
                "data": serializer.data,
                "message": "Art work fetched successfully"
            },
            status=200
        )



class KeyboardCategoryListView(APIView):
    permission_classes = [HasMobileThemeAPIKey]

    def get(self, request):
        categories = Category.objects.filter(type=Category.Type.KEYBOARD)

        skip, limit, error_response = get_pagination_params(request=request, default_limit=100)

        if error_response is not None:
            return error_response

        # total = categories.count()
        total = len(categories)

        categories = categories[skip:skip+limit]

        serializer = CategorySerializer(categories, many=True)

        return Response(
            {
                "status": 200,
                "data": {
                    "total": total,
                    "items": serializer.data,
                    "skip": skip,
                    "limit": limit
                },
                "message": "keyboard categories fetched successfully"
            }
        )

    

class KeyboardSubCategoryListView(APIView):
    permission_classes = [HasMobileThemeAPIKey]
    def get(self, request, category_id):
        category = Category.objects.filter(
            id=category_id,
            type=Category.Type.KEYBOARD,
        ).first()

        if category is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "Keyboard category no found",
                },
                status=404
            )

        subcategories = category.subcategories.all()
        # total = subcategories.count()
        total = len(subcategories)

        skip, limit, error_response = get_pagination_params(request=request, default_limit=100)

        if error_response is not None:
            return error_response
        
        subcategories = subcategories[skip:skip + limit]

        serializer = SubCategorySerializer(
            subcategories,
            many=True
        )

        return Response(
            {
                "status": 200,
                "data": {
                    "items": serializer.data,
                    "total": total,
                    "skip":  skip,
                    "limit": limit
                },
                "message": "Keyboard subcategories fetched successfully"
            },
            status=200
        )
        


class KeyboardListView(APIView):
    permission_classes = [HasMobileThemeAPIKey]
    def get(self, request):
        keyboards = Keyboard.objects.all().select_related(
            "category",
            "subcategory"
        )

        keyboards, error_response = apply_query_params_filters(request=request, query_set=keyboards)

        if error_response is not None:
            return error_response

        
        skip, limit, error_response = get_pagination_params(request=request, default_limit=20)

        if error_response is not None:
            return error_response

        # total = keyboards.count()
        total = len(keyboards)
        keyboards = keyboards[skip:skip+limit]

        serializer = KeyboardSerializer(
            keyboards,
            many=True
        )

        return Response(
            {
                "status": 200,
                "data": {
                    "items": serializer.data,
                    "total": total,
                    "skip": skip,
                    "limit": limit,
                },
                "message": "Keyboards fetched successfully"
            },
            status=200
        )



class KeyboardDetailView(APIView):
    permission_classes = [HasMobileThemeAPIKey]

    def get(self, request, keyboard_id):
        keyboard = Keyboard.objects.select_related(
            "category",
            "subcategory"
        ).filter(id=keyboard_id).first()

        if keyboard is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "Keyboard not found"
                },
                status=404
            )

        serializer = KeyboardSerializer(keyboard)

        return Response(
            {
                "status": 200,
                "data": serializer.data,
                "message": "Keyboard data fetched successfully"
            },
            status=200
        )
            

class WallpaperCategoryListView(APIView):
    permission_classes = [HasMobileThemeAPIKey]

    def get(self, request):
        categories = Category.objects.filter(
            type=Category.Type.WALLPAPER
        )

        skip, limit, error_response = get_pagination_params(request=request, default_limit=100)

        if error_response is not None:
            return error_response

        # total = categories.count()
        total = len(categories)

        categories = categories[skip:skip+limit]

        items = []

        for category in categories:
            items.append(
                {
                    "id": str(category.id),
                    "name": category.name,
                    "type": category.type,
                    "thumbnail": category.thumbnail,
                    "priority": category.priority,
                    "has_subcategories": category.subcategories.exists(),
                }
            )

        return Response(
            {
                "status": 200,
                "data": {
                    "items": items,
                    "total": total,
                    "skip": skip,
                    "limit": limit
                },
                "message": "Wallpaper categories fetched successfully"
            },
            status=200
        )


class WallpaperSubCategoryListView(APIView):
    permission_classes = [HasMobileThemeAPIKey]

    def get(self, request, category_id):
        category = Category.objects.filter(
            id=category_id,
            type=Category.Type.WALLPAPER
        ).first()

        if category is None:
            return Response(
                {
                    "status": 404,
                    "data":  None,
                    "message": "Catgeory does not exist"
                },
                status=404
            )

        skip, limit, error_response = get_pagination_params(request=request, default_limit=100)

        if error_response is not None:
            return error_response

        subcategories = category.subcategories.all()
        # total = subcategories.count()
        total = len(subcategories)
        subcategories = subcategories[skip:skip+limit]
        

        items =[]

        for subcategory in subcategories:
            item = {
                "id": str(subcategory.id),
                "name": subcategory.name,
                "thumbnail": subcategory.thumbnail,
                "priority": int(subcategory.priority)
            }

            items.append(item)

        return Response(
            {
                "status": 200,
                "data": {
                    "items": items,
                    "total": total,
                    "skip": skip,
                    "limit": limit
                },
                "message": "Wallpaper subcategories fetched successfully"
            },
            status=200
        )



class WallpaperListView(APIView):
    permission_classes = [HasMobileThemeAPIKey]

    def get(self, request):
        wallpapers = Wallpaper.objects.all().select_related(
            "category",
            "subcategory"
        )

        wallpapers, error_response = apply_query_params_filters(request=request, query_set=wallpapers)

        if error_response is not None:
            return error_response

        
        skip, limit, error_response = get_pagination_params(request=request, default_limit=20)

        if error_response is not None:
            return error_response

        # total = wallpapers.count()
        total = len(wallpapers)
        wallpapers = wallpapers[skip:skip+limit]

        items = []

        for wallpaper in wallpapers:
            item = {
                "id": str(wallpaper.id),
                "name": wallpaper.name,
                "category_id": wallpaper.category_id,
                "category_name": wallpaper.category.name,
                "subcategory_id": (
                    str(wallpaper.subcategory_id) if wallpaper.subcategory_id else None
                ),
                "subcategory_name": (
                    wallpaper.subcategory.name if wallpaper.subcategory else None
                ),
                "premium": wallpaper.premium,
                "preview_url": wallpaper.preview_url,
                "image_url": wallpaper.image_url,
                "priority": int(wallpaper.priority),
                "created_at": wallpaper.created_at
            }
            items.append(item)

        return Response(
            {
                "status": 200,
                "data": {
                    "items": items,
                    "total": total,
                    "skip": skip,
                    "limit": limit
                },
                "message": "Wallappers fetched successfully"
            },
            status=200
        )
    


class WallpaperDetailView(APIView):
    permission_classes = [HasMobileThemeAPIKey]

    def get(self, request, wallpaper_id):
        wallpaper = Wallpaper.objects.all().select_related(
            "category",
            "subcategory"
        ).filter(id=wallpaper_id).first()

        if wallpaper is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "This wallpaper does not exist"
                },
                status=404
            )

        data = {
            "id": str(wallpaper.id),
            "name": wallpaper.name,
            "category_id": wallpaper.category_id,
            "category_name": wallpaper.category.name,
            "subcategory_id": (
                str(wallpaper.subcategory_id) if wallpaper.subcategory_id else None
            ),
            "subcategory_name": (
                wallpaper.subcategory.name if wallpaper.subcategory else None
            ),
            "premium": wallpaper.premium,
            "preview_url": wallpaper.preview_url,
            "image_url": wallpaper.image_url,
            "priority": int(wallpaper.priority),
            "created_at": wallpaper.created_at
        }

        return Response(
            {
                "status": 200,
                "data": data,
                "message": "wallpaper fetched successfully"
            },
            status=200
        )

        

class ThemeCategoryListView(APIView):
    permission_classes = [HasMobileThemeAPIKey]

    def get(self, request):
        categories = Category.objects.filter(type=Category.Type.THEME)

        skip, limit, error_response = get_pagination_params(request=request, default_limit=100)

        if error_response is not None:
            return error_response
        
        # total = categories.count()
        total = len(categories)

        categories = categories[skip:skip+limit]

        items = []

        for category in categories:
            item = {
                "id": category.id,
                "name": category.name,
                "type":  category.type,
                "thumbnail": category.thumbnail,
                "priority": int(category.priority),
                "has_subcategories": category.subcategories.exists()
            }
            items.append(item)

        
        return Response(
            {
                "status": 200,
                "data": {
                    "items": items,
                    "total": total,
                    "skip": skip,
                    "limit": limit
                },
                "message": "Theme  categories fetches successfully"
            },
            status=200
        )

    
class ThemeSubcategoryListView(APIView):
    permission_classes = [HasMobileThemeAPIKey]

    def get(self, request, category_id):
        category = Category.objects.filter(
            id=category_id,
            type=Category.Type.THEME
        ).first()

        if category is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "Category not found"
                },
                status=404
            )

        skip, limit, error_response = get_pagination_params(request=request, default_limit=100)

        if error_response is not None:
            return error_response

        subcategories = category.subcategories.all()
        # total = subcategories.count()
        total = len(subcategories)
        subcategories = subcategories[skip:skip+limit]

        items = []

        for subcategory in subcategories:
            item = {
                "id": subcategory.id,
                "name": subcategory.name,
                "thumbnail": subcategory.thumbnail,
                "priority": subcategory.priority
            }
            items.append(item)

        return Response(
            {
                "status": 200,
                "data": {
                    "items": items,
                    "total": total,
                    "skip": skip,
                    "limit": limit
                },
                "message": "theme subcategories fetched successfully"
            },
            status=200
        )



class ThemeListView(APIView):
    permission_classes = [HasMobileThemeAPIKey]

    def get(self, request):
        themes = Theme.objects.all().select_related(
            "category",
            "subcategory",
            "keyboard",
            "wallpaper"
        ).prefetch_related("icons")


        themes, error_response = apply_query_params_filters(request=request, query_set=themes)

        if error_response is not None:
            return error_response

        
        skip, limit, error_response = get_pagination_params(request=request, default_limit=20)

        if error_response is not None:
            return error_response

        # total = themes.count()
        total = len(themes)
        themes = themes[skip:skip+limit]

        items = []

        for theme in themes:
            keyboard_data = None
            wallpaper_data = None
            icon_items = []
            if theme.keyboard:
                keyboard_data = {
                    "id": str(theme.keyboard.id),
                    "name": theme.keyboard.name,
                    "preview_url": theme.keyboard.preview_url,
                    "text_color": theme.keyboard.text_color,
                    "key_alpha": theme.keyboard.key_alpha,
                    "keyboard_bg": theme.keyboard.keyboard_bg,
                    "normal_key_bg": theme.keyboard.normal_key_bg,
                    "specialty_keys_bg": theme.keyboard.specialty_keys_bg,
                }

            if theme.wallpaper:
                wallpaper_data = {
                    "id": str(theme.wallpaper.id),
                    "name": theme.wallpaper.name,
                    "preview_url": theme.wallpaper.preview_url,
                    "image_url": theme.wallpaper.image_url,
                }



            for icon in theme.icons.all():
                        icon_data = {
                            "id": str(icon.id),
                            "name": icon.name,
                            "preview_url": icon.preview_url,
                            "icon_image": icon.icon_image,
                            "alias_id": icon.alias_id,
                            "priority": icon.priority,
                            "created_at": icon.created_at,
                        }
                        icon_items.append(icon_data)


            
            item = {
                "id": theme.id,
                "name": theme.name,
                "category_id": theme.category_id,
                "category_name": theme.category.name,
                "subcategory_id": (
                    theme.subcategory_id if theme.subcategory_id else None
                ),
                "subcategory_name": (
                    theme.subcategory.name if theme.subcategory else None
                ),
                "premium": theme.premium,
                "preview_url": theme.preview_url,
                "keyboard_id": (
                    theme.keyboard_id if theme.keyboard_id else None
                ),
                "wallpaper_id" :(
                    theme.wallpaper_id if theme.wallpaper_id else None
                ),
                "keyboard": keyboard_data,
                "wallpaper": wallpaper_data,
                "icons": icon_items,
                "priority": theme.priority,
                "created_at": theme.created_at
            }

            items.append(item)

        return Response(
            {
                "status": 200,
                "data": {
                    "items": items,
                    "total": total,
                    "skip": skip,
                    "limit": limit
                },
                "message": "themes list fetched successfully"
            },
            status=200
        )

        
class ThemeDetailView(APIView):
    permission_classes = [HasMobileThemeAPIKey]

    def get(self, request, theme_id):
        theme = Theme.objects.all().select_related(
            "category",
            "subcategory",
            "keyboard",
            "wallpaper"
        ).prefetch_related("icons").filter(id=theme_id).first()


        if theme is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "No theme found"
                },
                status=404
            )
        

        keyboard_data = None
        wallpaper_data = None
        icon_items = []


        if theme.keyboard:
            keyboard_data = {
                        "id": str(theme.keyboard.id),
                        "name": theme.keyboard.name,
                        "preview_url": theme.keyboard.preview_url,
                        "text_color": theme.keyboard.text_color,
                        "key_alpha": theme.keyboard.key_alpha,
                        "keyboard_bg": theme.keyboard.keyboard_bg,
                        "normal_key_bg": theme.keyboard.normal_key_bg,
                        "specialty_keys_bg": theme.keyboard.specialty_keys_bg,
                    }

        if theme.wallpaper:
            wallpaper_data = {
                        "id": str(theme.wallpaper.id),
                        "name": theme.wallpaper.name,
                        "preview_url": theme.wallpaper.preview_url,
                        "image_url": theme.wallpaper.image_url,
                    }


        for icon in theme.icons.all():
            icon_data = {
                "id": str(icon.id),
                "name": icon.name,
                "preview_url": icon.preview_url,
                "icon_image": icon.icon_image,
                "alias_id": icon.alias_id,
                "priority": icon.priority,
                "created_at": icon.created_at,
            }
            icon_items.append(icon_data)
            
        
        data = {
                "id": theme.id,
                "name": theme.name,
                "category_id": theme.category_id,
                "category_name": theme.category.name,
                "subcategory_id": (
                    theme.subcategory_id if theme.subcategory_id else None
                ),
                "subcategory_name": (
                    theme.subcategory.name if theme.subcategory else None
                ),
                "premium": theme.premium,
                "preview_url": theme.preview_url,
                "keyboard_id": (
                    theme.keyboard_id if theme.keyboard_id else None
                ),
                "wallpaper_id" :(
                    theme.wallpaper_id if theme.wallpaper_id else None
                ),
                "keyboard": keyboard_data,
                "wallpaper": wallpaper_data,
                "icons": icon_items,
                "priority": theme.priority,
                "created_at": theme.created_at
            }

        
        return Response(
            {
                "status": 200,
                "data": data,
                "message": "theme item fetched successfully"
            },
            status=200
        )

        
class DiyImageListView(APIView):
    permission_classes = [HasMobileThemeAPIKey]
    def get(self, request):
        images = DiyImage.objects.all()

        skip, limit, error_response = get_pagination_params(request=request, default_limit=20)

        if error_response is not None:
            return error_response

        # total = images.count()
        total = len(images)

        images = images[skip:skip+limit]

        serializer = DiyImageSerializer(images, many=True)

        return Response(
            {
                "status": 200,
                "data": {
                    "items": serializer.data,
                    "total": total,
                    "skip": skip,
                    "limit": limit,
                },
                "message": "DIY Images data fetched successfully"
            },
            status=200
        )


class DiyImageDetailView(APIView):
    permission_classes = [HasMobileThemeAPIKey]
    def get(self, request, image_id):
        image = DiyImage.objects.filter(id=image_id).first()

        if image is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "No image found against this ID"
                },
                status=404
            )

        serializer = DiyImageSerializer(image)

        return Response(
            {
                "status": 200,
                "data": serializer.data,
                "message": "Image against this id fetched successfully"
            },
            status=200
        )



class DiyFontListView(APIView):
    permission_classes = [HasMobileThemeAPIKey]

    def get(self, request):
        fonts = DiyFont.objects.all()

        skip, limit, error_response = get_pagination_params(request=request, default_limit=20)

        if error_response is not None:
            return error_response

        # total = fonts.count()
        total = len(fonts)
        fonts = fonts[skip:skip+limit]

        serializer = DiyFontSerilaizer(fonts, many=True)

        return Response(
            {
                "status": 200,
                "data": {
                    "items": serializer.data,
                    "total": total,
                    "skip": skip,
                    "limit": limit
                },
                "message": "fonts data fetched successfully"
            },
            status=200
        )


class DiyFontDetailView(APIView):
    permission_classes = [HasMobileThemeAPIKey]

    def get(self, request, font_id):
        font = DiyFont.objects.filter(id=font_id).first()

        if font is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "No data found against this font id"
                },
                status=404
            )   

        serializer = DiyFontSerilaizer(font)

        return Response(
            {
                "status": 200,
                "data": serializer.data,
                "message": "Font detail fetched successfully"
            },
            status=200
        )    



class DiyEffectListView(APIView):
    permission_classes = [HasMobileThemeAPIKey]

    def get(self, request):
        effects = DiyEffect.objects.all()

        skip, limit, error_response = get_pagination_params(request=request, default_limit=20)

        if error_response is not None:
            return error_response

        # total = effects.count()
        total = len(effects)
        effects = effects[skip:skip+limit]

        serializer = DiyEffectSerializer(effects, many=True)

        return Response(
            {
                "status": 200,
                "data": {
                    "items": serializer.data,
                    "total": total,
                    "skip": skip,
                    "limit": limit
                },
                "message": "effects data fetched successfully"
            },
            status=200
        )



class DiyEffectDetailView(APIView):
    permission_classes = [HasMobileThemeAPIKey]

    def get(self, request, effect_id):
        effect = DiyEffect.objects.filter(id=effect_id).first()

        if effect is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "No data exists against this id"
                },
                status=404
            )

        serializer = DiyEffectSerializer(effect)

        return Response(
            {
                "status": 200,
                "data": serializer.data,
                "message": "Effect fetched successfully"
            },
            status=200
        )


class DiyKeyListView(APIView):
    permission_classes = [HasMobileThemeAPIKey]

    def get(self, request):
        keys = DiyKey.objects.all()

        skip, limit, error_response = get_pagination_params(request=request, default_limit=20)

        if error_response is not None:
            return error_response

        # total = keys.count()
        total = len(keys)
        keys = keys[skip:skip+limit]

        serializer = DiyKeySerializer(keys, many=True)

        return Response(
            {
                "status": 200,
                "data": {
                    "items": serializer.data,
                    "total": total,
                    "skip": skip,
                    "limit": limit
                },
                "message": "Diy Keys data fetched successfully"
            },
            status=200
        )



class DiyKeyDetailView(APIView):
    permission_classes = [HasMobileThemeAPIKey]

    def get(self, request, key_id):
        key = DiyKey.objects.filter(id=key_id).first()

        if key is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "No key found against this id"
                },
                status=404
            )

        serializer = DiyKeySerializer(key)

        return Response(
            {
                "status": 200,
                "data": serializer.data,
                "message": "Key details fetched successfully"
            },
            status=200
        )



class DiySoundListView(APIView):
    permission_classes = [HasMobileThemeAPIKey]

    def get(self, request):
        sounds = DiySound.objects.all()

        skip, limit, error_response = get_pagination_params(request=request, default_limit=20)

        if error_response is  not None:
            return error_response


        # total = sounds.count()
        total = len(sounds)
        sounds = sounds[skip:skip+limit]

        serializer = DiySoundSerializer(sounds, many=True)

        return Response(
            {
                "status": 200,
                "data": {
                    "items": serializer.data,
                    "total": total,
                    "skip": skip,
                    "limit": limit
                },
                "message": "Diy sounds data fetched successfully"
            },
            status=200
        )



class DiySoundDetailView(APIView):
    permission_classes = [HasMobileThemeAPIKey]

    def get(self, request, sound_id):
        sound = DiySound.objects.filter(id=sound_id).first()

        if sound is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "No sound found against this id"
                },
                status=404
            )

        serializer = DiySoundSerializer(sound)

        return Response(
            {
                "status": 200,
                "data": serializer.data,
                "message": "Diy sound data fetched successfully"
            },
            status=200
        )



