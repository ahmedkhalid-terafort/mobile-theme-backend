from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Category, CoolFont, Keyboard, Wallpaper, Theme,
    DiyImage, DiyFont, DiyEffect, DiyKey, DiySound
)
from.permissions import HasMobileThemeAPIKey
from .serializers import (
    CategorySerializer, SubCategorySerializer,
    CoolFontSerializer,
    KeyboardSerializer,
    WallpaperSerializer,
    ThemeSerializer,
    DiyImageSerializer,
    DiyFontSerilaizer,
    DiyEffectSerializer,
    DiyKeySerializer,
    DiySoundSerializer
)
from .services.cache import get_cached_items, set_cached_items
from .utils import get_pagination_params
from .utils_v2 import apply_cached_items_filters


class ArtWorkCategoryListViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request):
        skip, limit, error_response = get_pagination_params(request, default_limit=100)
        if error_response:
            return error_response

        cache_key = "catalog:artwork_categories"
        items = get_cached_items(cache_key)

        if items is None:
            categories = Category.objects.filter(
                type=Category.Type.COOL_FONT
            )

            serializer = CategorySerializer(categories, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        total = len(items)
        paginated_items = items[skip:skip+limit]

        return Response(
            {
                "status": 200,
                "data": {
                    "items": paginated_items,
                    "total": total,
                    "skip": skip,
                    "limit": limit
                },
                "message": "Artwork categories fetched successfully."
            },
            status=200
        )

        
class ArtWorkSubCategoryListViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request, category_id):
        skip, limit, error_response = get_pagination_params(request, default_limit=100)
        if error_response:
            return error_response

        cache_key = f"catalog:artwork_subcategories:{category_id}"
        items = get_cached_items(cache_key)

        if items is None:
            category = Category.objects.filter(
                id=category_id,
                type=Category.Type.COOL_FONT
            ).first()

            if category is None:
                return Response(
                    {
                        "status": 404,
                        "data": None,
                        "message": "Artwork category not found"
                    },
                    status=404
                )

            subcategories = category.subcategories.all()
            serializer = SubCategorySerializer(subcategories, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        total = len(items)
        paginated_items = items[skip:skip+limit]

        return Response(
            {
                "status": 200,
                "data": {
                    "items": paginated_items,
                    "total": total,
                    "skip": skip,
                    "limit": limit
                },
                "message": "Artwork subcategories fetchted successfully"
            },
            status=200
        )
    

class ArtWorkListViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request):
        skip, limit, error_response = get_pagination_params(request, default_limit=20)
        if error_response:
            return error_response

        cache_key = "catalog:artworks"
        items = get_cached_items(cache_key)

        if items is None:
            artworks = CoolFont.objects.all().select_related("category", "subcategory")
            serializer = CoolFontSerializer(artworks, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        filtered_items, error_response = apply_cached_items_filters(request, items)
        if error_response:
            return error_response

        total = len(filtered_items)
        paginated_items = filtered_items[skip:skip+limit]

        return Response(
            {
                "status": 200,
                "data": {
                    "items": paginated_items,
                    "total": total,
                    "skip": skip,
                    "limit": limit
                },
                "message": "Artworks fetched successfully"
            },
            status=200
        )


class ArtWorkDetailViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request, artwork_id):
        cache_key = "catalog:artworks"
        items = get_cached_items(cache_key)

        if items is None:
            artworks = CoolFont.objects.select_related("category", "subcategory").all()
            serializer = CoolFont(artworks, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        single_item = None
        for item in items:
            if str(item.get("id")) == str(artwork_id):
                single_item = item
                break

        if single_item is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "Artwork not found"
                },
                status=404
            )

        return Response(
            {
                "status": 200,
                "data": single_item,
                "message": "Artwork fetched successfully"
            },
            status=200
        )


class KeyboardCategoryListViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request):
        skip, limit, error_response = get_pagination_params(request, default_limit=100)
        if error_response:
            return error_response

        cache_key = "catalog:keyboard_categories"
        items = get_cached_items(cache_key)

        if items is None:
            categories = Category.objects.filter(type=Category.Type.KEYBOARD)
            serializer = CategorySerializer(categories, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        total = len(items)
        paginated_items = items[skip:skip+limit]

        return Response(
            {
                "status": 200,
                "data": {
                    "items": paginated_items,
                    "total": total,
                    "skip": skip,
                    "limit": limit,
                },
                "message": "Keyboard categories fetched successfully"
            },
            status=200
        )


class KeyboardSubcategoryListViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request, category_id):
        skip, limit, error_response = get_pagination_params(request, default_limit=100)
        if error_response:
            return error_response

        cache_key = f"catalog:keyboard_subcategories:{category_id}"
        items = get_cached_items(cache_key)
        if items is None:
            category = Category.objects.filter(
                id=category_id,
                type=Category.Type.KEYBOARD,
            ).first()

            if category is None:
                return Response(
                    {
                        "status": 404,
                        "data": None,
                        "message": "Keyboard category not found"
                    },
                    status=404
                )
            subcategories = category.subcategories.all()
            serializer = SubCategorySerializer(subcategories, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        total = len(items)
        paginated_items = items[skip:skip+limit]

        return Response(
            {
                "status": 200,
                "data": {
                    "items": paginated_items,
                    "total": total,
                    "skip": skip,
                    "limit": limit
                },
                "message": "Keyboard subcategories fetched successfully"
            },
            status=200
        )


class KeyboardListViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request):
        skip, limit, error_response = get_pagination_params(request, default_limit=20)
        if error_response:
            return error_response

        cache_key = "catalog:keyboards"
        items = get_cached_items(cache_key)
        if items is None:
            keyboards = Keyboard.objects.all().select_related(
                "category",
                "subcategory"
            )
            serializer = KeyboardSerializer(keyboards, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        filtered_items, error_response = apply_cached_items_filters(request, items)
        if error_response:
            return error_response

        total = len(filtered_items)
        paginated_items = filtered_items[skip:skip+limit]

        return Response(
            {
                "status": 200,
                "data": {
                    "items": paginated_items,
                    "total": total,
                    "skip": skip,
                    "limit": limit
                },
                "message": "Keyboards data fetched successfully"
            },
            status=200
        )


class KeyboardDetailViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request, keyboard_id):
        cache_key = "catalog:keyboards"
        items = get_cached_items(cache_key)
        if items is None:
            keyboards = Keyboard.objects.all().select_related("category", "subcategory")
            serializer = KeyboardSerializer(keyboards, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        single_item = None

        for item in items:
            if str(item.get("id")) == str(keyboard_id):
                single_item = item
                break

        if single_item is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "No data found against this id"
                },
                status=404
            )

        return Response(
            {
                "status": 200,
                "data": single_item,
                "message": "Data fetched successfully"
            },
            status=200
        )


class WallpaperCategoryListViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request):
        skip, limit, error_response = get_pagination_params(
            request,
            default_limit=100,
        )
        if error_response:
            return error_response

        cache_key = "catalog:wallpaper_categories"
        items = get_cached_items(cache_key)

        if items is None:
            categories = Category.objects.filter(
                type=Category.Type.WALLPAPER,
            )
            serializer = CategorySerializer(categories, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        total = len(items)
        paginated_items = items[skip:skip + limit]

        return Response(
            {
                "status": 200,
                "data": {
                    "items": paginated_items,
                    "total": total,
                    "skip": skip,
                    "limit": limit,
                },
                "message": "Wallpaper categories fetched successfully",
            },
            status=200,
        )


class WallpaperSubcategoryListViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request, category_id):
        skip, limit, error_response = get_pagination_params(
            request,
            default_limit=100,
        )
        if error_response:
            return error_response

        cache_key = f"catalog:wallpaper_subcategories:{category_id}"
        items = get_cached_items(cache_key)

        if items is None:
            category = Category.objects.filter(
                id=category_id,
                type=Category.Type.WALLPAPER,
            ).first()

            if category is None:
                return Response(
                    {
                        "status": 404,
                        "data": None,
                        "message": "Wallpaper category not found",
                    },
                    status=404,
                )

            subcategories = category.subcategories.all()
            serializer = SubCategorySerializer(subcategories, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        total = len(items)
        paginated_items = items[skip:skip + limit]

        return Response(
            {
                "status": 200,
                "data": {
                    "items": paginated_items,
                    "total": total,
                    "skip": skip,
                    "limit": limit,
                },
                "message": "Wallpaper subcategories fetched successfully",
            },
            status=200,
        )


class WallpaperListViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request):
        skip, limit, error_response = get_pagination_params(
            request,
            default_limit=20,
        )
        if error_response:
            return error_response

        cache_key = "catalog:wallpapers"
        items = get_cached_items(cache_key)

        if items is None:
            wallpapers = Wallpaper.objects.select_related(
                "category",
                "subcategory",
            ).all()
            serializer = WallpaperSerializer(wallpapers, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        filtered_items, error_response = apply_cached_items_filters(
            request,
            items,
        )
        if error_response:
            return error_response

        total = len(filtered_items)
        paginated_items = filtered_items[skip:skip + limit]

        return Response(
            {
                "status": 200,
                "data": {
                    "items": paginated_items,
                    "total": total,
                    "skip": skip,
                    "limit": limit,
                },
                "message": "Wallpapers fetched successfully",
            },
            status=200,
        )


class WallpaperDetailViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request, wallpaper_id):
        cache_key = "catalog:wallpapers"
        items = get_cached_items(cache_key)

        if items is None:
            wallpapers = Wallpaper.objects.select_related(
                "category",
                "subcategory",
            ).all()
            serializer = WallpaperSerializer(wallpapers, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        single_item = None

        for item in items:
            if str(item.get("id")) == str(wallpaper_id):
                single_item = item
                break

        if single_item is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "Wallpaper not found",
                },
                status=404,
            )

        return Response(
            {
                "status": 200,
                "data": single_item,
                "message": "Wallpaper fetched successfully",
            },
            status=200,
        )


class ThemeCategoryListViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request):
        skip, limit, error_response = get_pagination_params(
            request,
            default_limit=100,
        )
        if error_response:
            return error_response

        cache_key = "catalog:theme_categories"
        items = get_cached_items(cache_key)

        if items is None:
            categories = Category.objects.filter(
                type=Category.Type.THEME,
            )
            serializer = CategorySerializer(categories, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        total = len(items)
        paginated_items = items[skip:skip + limit]

        return Response(
            {
                "status": 200,
                "data": {
                    "items": paginated_items,
                    "total": total,
                    "skip": skip,
                    "limit": limit,
                },
                "message": "Theme categories fetched successfully",
            },
            status=200,
        )


class ThemeSubcategoryListViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request, category_id):
        skip, limit, error_response = get_pagination_params(
            request,
            default_limit=100,
        )
        if error_response:
            return error_response

        cache_key = f"catalog:theme_subcategories:{category_id}"
        items = get_cached_items(cache_key)

        if items is None:
            category = Category.objects.filter(
                id=category_id,
                type=Category.Type.THEME,
            ).first()

            if category is None:
                return Response(
                    {
                        "status": 404,
                        "data": None,
                        "message": "Theme category not found",
                    },
                    status=404,
                )

            subcategories = category.subcategories.all()
            serializer = SubCategorySerializer(subcategories, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        total = len(items)
        paginated_items = items[skip:skip + limit]

        return Response(
            {
                "status": 200,
                "data": {
                    "items": paginated_items,
                    "total": total,
                    "skip": skip,
                    "limit": limit,
                },
                "message": "Theme subcategories fetched successfully",
            },
            status=200,
        )


class ThemeListViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request):
        skip, limit, error_response = get_pagination_params(
            request,
            default_limit=20,
        )
        if error_response:
            return error_response

        cache_key = "catalog:themes"
        items = get_cached_items(cache_key)

        if items is None:
            themes = Theme.objects.select_related(
                "category",
                "subcategory",
                "keyboard",
                "wallpaper",
            ).prefetch_related("icons")
            serializer = ThemeSerializer(themes, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        filtered_items, error_response = apply_cached_items_filters(
            request,
            items,
        )
        if error_response:
            return error_response

        total = len(filtered_items)
        paginated_items = filtered_items[skip:skip + limit]

        return Response(
            {
                "status": 200,
                "data": {
                    "items": paginated_items,
                    "total": total,
                    "skip": skip,
                    "limit": limit,
                },
                "message": "Themes fetched successfully",
            },
            status=200,
        )


class ThemeDetailViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request, theme_id):
        cache_key = "catalog:themes"
        items = get_cached_items(cache_key)

        if items is None:
            themes = Theme.objects.select_related(
                "category",
                "subcategory",
                "keyboard",
                "wallpaper",
            ).prefetch_related("icons")
            serializer = ThemeSerializer(themes, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        single_item = None

        for item in items:
            if str(item.get("id")) == str(theme_id):
                single_item = item
                break

        if single_item is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "Theme not found",
                },
                status=404,
            )

        return Response(
            {
                "status": 200,
                "data": single_item,
                "message": "Theme fetched successfully",
            },
            status=200,
        )


class DiyImageListViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request):
        skip, limit, error_response = get_pagination_params(
            request,
            default_limit=20,
        )
        if error_response:
            return error_response

        cache_key = "catalog:diy_images"
        items = get_cached_items(cache_key)

        if items is None:
            images = DiyImage.objects.all()
            serializer = DiyImageSerializer(images, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        total = len(items)
        paginated_items = items[skip:skip + limit]

        return Response(
            {
                "status": 200,
                "data": {
                    "items": paginated_items,
                    "total": total,
                    "skip": skip,
                    "limit": limit,
                },
                "message": "DIY images fetched successfully",
            },
            status=200,
        )


class DiyImageDetailViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request, image_id):
        cache_key = "catalog:diy_images"
        items = get_cached_items(cache_key)

        if items is None:
            images = DiyImage.objects.all()
            serializer = DiyImageSerializer(images, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        single_item = None
        for item in items:
            if str(item.get("id")) == str(image_id):
                single_item = item
                break

        if single_item is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "DIY image not found",
                },
                status=404,
            )

        return Response(
            {
                "status": 200,
                "data": single_item,
                "message": "DIY image fetched successfully",
            },
            status=200,
        )


class DiyFontListViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request):
        skip, limit, error_response = get_pagination_params(
            request,
            default_limit=20,
        )
        if error_response:
            return error_response

        cache_key = "catalog:diy_fonts"
        items = get_cached_items(cache_key)

        if items is None:
            fonts = DiyFont.objects.all()
            serializer = DiyFontSerilaizer(fonts, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        total = len(items)
        paginated_items = items[skip:skip + limit]

        return Response(
            {
                "status": 200,
                "data": {
                    "items": paginated_items,
                    "total": total,
                    "skip": skip,
                    "limit": limit,
                },
                "message": "DIY fonts fetched successfully",
            },
            status=200,
        )


class DiyFontDetailViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request, font_id):
        cache_key = "catalog:diy_fonts"
        items = get_cached_items(cache_key)

        if items is None:
            fonts = DiyFont.objects.all()
            serializer = DiyFontSerilaizer(fonts, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        single_item = None
        for item in items:
            if str(item.get("id")) == str(font_id):
                single_item = item
                break

        if single_item is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "DIY font not found",
                },
                status=404,
            )

        return Response(
            {
                "status": 200,
                "data": single_item,
                "message": "DIY font fetched successfully",
            },
            status=200,
        )


class DiyEffectListViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request):
        skip, limit, error_response = get_pagination_params(
            request,
            default_limit=20,
        )
        if error_response:
            return error_response

        cache_key = "catalog:diy_effects"
        items = get_cached_items(cache_key)

        if items is None:
            effects = DiyEffect.objects.all()
            serializer = DiyEffectSerializer(effects, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        total = len(items)
        paginated_items = items[skip:skip + limit]

        return Response(
            {
                "status": 200,
                "data": {
                    "items": paginated_items,
                    "total": total,
                    "skip": skip,
                    "limit": limit,
                },
                "message": "DIY effects fetched successfully",
            },
            status=200,
        )


class DiyEffectDetailViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request, effect_id):
        cache_key = "catalog:diy_effects"
        items = get_cached_items(cache_key)

        if items is None:
            effects = DiyEffect.objects.all()
            serializer = DiyEffectSerializer(effects, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        single_item = None
        for item in items:
            if str(item.get("id")) == str(effect_id):
                single_item = item
                break

        if single_item is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "DIY effect not found",
                },
                status=404,
            )

        return Response(
            {
                "status": 200,
                "data": single_item,
                "message": "DIY effect fetched successfully",
            },
            status=200,
        )


class DiyKeyListViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request):
        skip, limit, error_response = get_pagination_params(
            request,
            default_limit=20,
        )
        if error_response:
            return error_response

        cache_key = "catalog:diy_keys"
        items = get_cached_items(cache_key)

        if items is None:
            keys = DiyKey.objects.all()
            serializer = DiyKeySerializer(keys, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        total = len(items)
        paginated_items = items[skip:skip + limit]

        return Response(
            {
                "status": 200,
                "data": {
                    "items": paginated_items,
                    "total": total,
                    "skip": skip,
                    "limit": limit,
                },
                "message": "DIY keys fetched successfully",
            },
            status=200,
        )


class DiyKeyDetailViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request, key_id):
        cache_key = "catalog:diy_keys"
        items = get_cached_items(cache_key)

        if items is None:
            keys = DiyKey.objects.all()
            serializer = DiyKeySerializer(keys, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        single_item = None
        for item in items:
            if str(item.get("id")) == str(key_id):
                single_item = item
                break

        if single_item is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "DIY key not found",
                },
                status=404,
            )

        return Response(
            {
                "status": 200,
                "data": single_item,
                "message": "DIY key fetched successfully",
            },
            status=200,
        )


class DiySoundListViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request):
        skip, limit, error_response = get_pagination_params(
            request,
            default_limit=20,
        )
        if error_response:
            return error_response

        cache_key = "catalog:diy_sounds"
        items = get_cached_items(cache_key)

        if items is None:
            sounds = DiySound.objects.all()
            serializer = DiySoundSerializer(sounds, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        total = len(items)
        paginated_items = items[skip:skip + limit]

        return Response(
            {
                "status": 200,
                "data": {
                    "items": paginated_items,
                    "total": total,
                    "skip": skip,
                    "limit": limit,
                },
                "message": "DIY sounds fetched successfully",
            },
            status=200,
        )


class DiySoundDetailViewV2(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request, sound_id):
        cache_key = "catalog:diy_sounds"
        items = get_cached_items(cache_key)

        if items is None:
            sounds = DiySound.objects.all()
            serializer = DiySoundSerializer(sounds, many=True)
            items = list(serializer.data)
            set_cached_items(cache_key, items)

        single_item = None
        for item in items:
            if str(item.get("id")) == str(sound_id):
                single_item = item
                break

        if single_item is None:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "message": "DIY sound not found",
                },
                status=404,
            )

        return Response(
            {
                "status": 200,
                "data": single_item,
                "message": "DIY sound fetched successfully",
            },
            status=200,
        )

