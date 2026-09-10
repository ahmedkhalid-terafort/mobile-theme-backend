from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, CoolFont, Keyboard, Wallpaper, Theme
from .permissions import HasMobileThemeAPIKey
from .serializers import (
    CategorySerializer,
    CoolFontSerializer,
    SubCategorySerializer,
    KeyboardSerializer
)


class ArtworkCategoryListView(APIView):
    permission_classes = (HasMobileThemeAPIKey,)

    def get(self, request):
        categories = Category.objects.filter(
            type=Category.Type.COOL_FONT,
        )

        try:
            skip = int(request.query_params.get("skip", 0))
            limit = int(request.query_params.get("limit", 100))
        except ValueError:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "Skip and limit must be integers.",
                },
                status=422,
            )

        if skip < 0 or limit < 1 or limit > 100:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "Skip must be 0 or greater, and limit must be 1 or greater.",
                },
                status=422
            )

        total = categories.count()

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

        try:
            skip = int(request.query_params.get("skip", 0))
            limit = int(request.query_params.get("limit", 100))
        except ValueError:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "Skip and limit must be integers.",
                },
                status=422
            ) 

        if skip < 0 or limit < 1 or limit > 100:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "Skip must be 0 or greater, and limit must be between 1 and 100.",
                },
                status=422
            )

        subcategories = category.subcategories.all()
        total = subcategories.count()
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
    permission_classes = [HasMobileThemeAPIKey]

    def get(self, request):
        artworks = CoolFont.objects.select_related(
            "category",
            "subcategory"
        ).all()

        category_id = request.query_params.get("category_id")
        subcategory_id = request.query_params.get("subcategory_id")
        premium_only = request.query_params.get(
            "premium_only",
            "false"
        ).lower()

        if subcategory_id:
            artworks = artworks.filter(
                subcategory_id=subcategory_id,
            )
        elif category_id:
            artworks = artworks.filter(
                category_id=category_id,
                subcategory__isnull=True,
            )

        if premium_only not in ("true", "false"):
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "premium_only must be true or false.",
                },
                status=422,
            )

        if premium_only == "true":
            artworks = artworks.filter(premium=True)

        try:
            skip = int(request.query_params.get("skip", 0))
            limit = int(request.query_params.get("limit", 20))
        except ValueError:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "Skip and limit must be integers.",
                },
                status=422,
            )

        if skip < 0 or limit < 1 or limit > 100:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "Skip must be 0 or greater, and limit must be between 1 and 100.",
                },
                status=422,
            )

        total = artworks.count()
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

        try:
            skip = int(request.query_params.get("skip", 0))
            limit = int(request.query_params.get("limit", 100))
        except ValueError:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "skip and limit must be integers"
                },
                status=422
            )

        if skip < 0 or limit > 100:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "skip must not be negative and max limit is 100"
                },
                status=422
            )

        total = categories.count()

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
        total = subcategories.count()

        try:
            skip = int(request.query_params.get("skip", 0))
            limit =  int(request.query_params.get("limit", 100))
        except ValueError:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "skip and limit must be integers"
                },
                status=422
            )

        if skip < 0 or limit > 100:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "Skip must not be less than 0 and max limit is 100"
                },
                status=422
            )

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

        category_id = request.query_params.get("category_id")
        subcategory_id = request.query_params.get("subcategory_id")
        premium_only = request.query_params.get("premium_only", "false").lower()

        if subcategory_id:
            keyboards = keyboards.filter(subcategory_id=subcategory_id)
        elif category_id:
            keyboards = keyboards.filter(category_id=category_id, subcategory__isnull=True)

        if premium_only == "true":
            keyboards = keyboards.filter(premium=True)

        try:
            skip = int(request.query_params.get("skip", 0))
            limit = int(request.query_params.get("limit", 20))
        except ValueError:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "Skip amd limit must be integers."
                },
                status=422
            )

        if skip < 0 or limit > 100:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "skip must not be negative and max limit is 100"
                },
                status=422
            )

        total = keyboards.count()
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

        try:
            skip = int(request.query_params.get("skip", 0))
            limit = int(request.query_params.get("limit", 100))
        except ValueError:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "skip and limit must be integers"
                },
                status=422
            )

        if skip < 0 or limit < 1 or limit > 100:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "skip must be positive and limit must be between 1 and 100"
                },
                status=422
            )

        total = categories.count()

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

        try:
            skip = int(request.query_params.get("skip", 0))
            limit = int(request.query_params.get("limit", 100))
        except ValueError:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "skip and limit must be integers"
                },
                status=422
            )

        if skip < 0 or limit < 1 or limit > 100:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "skip must not be zero and limit must be between 1 and 100"
                },
                status=422
            )

        subcategories = category.subcategories.all()
        total = subcategories.count()
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

        category_id = request.query_params.get("category_id")
        subcategory_id = request.query_params.get("subcategory_id")
        premium_only = request.query_params.get("premium_only", "false").lower()

        if subcategory_id:
            wallpapers = wallpapers.filter(subcategory_id=subcategory_id)
        elif category_id:
            wallpapers = wallpapers.filter(category_id=category_id, subcategory__isnull=True,)

        if premium_only == "true":
            wallpapers = wallpapers.filter(premium=True)

        try:
            skip = int(request.query_params.get("skip", 0))
            limit = int(request.query_params.get("limit", 20))
        except ValueError:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "skip and limit must be integers"
                },
                status=422
            )

        if skip < 0 or limit < 1 or limit > 100:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "skip can not be less than 0 and limit must be between 1 and 100"
                },
                status=422
            )

        total = wallpapers.count()
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

        try:
            skip = int(request.query_params.get("skip", 0))
            limit = int(request.query_params.get("limit", 100))
        except ValueError:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "skip and limit must be integers"
                },
                status=422
            )

        if skip < 0 or limit < 1 or limit > 100:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "skip must not be negative and limit  must be between 1 and 100"
                },
                status=422
            )

        total = categories.count()

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

        try:
            skip = int(request.query_params.get("skip", 0))
            limit = int(request.query_params.get("limit", 100))
        except ValueError:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "skip and limit must be integers"
                },
                status=422
            )

        if skip < 0 or limit < 1 or limit > 100:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "skip must be greater than 0 and limit must be between 1 and 100"
                },
                status=422
            )

        subcategories = category.subcategories.all()
        total = subcategories.count()
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

        category_id = request.query_params.get("category_id")
        subcategory_id = request.query_params.get("subcategory_id")
        premium_only = request.query_params.get("premium_only", "false").lower()

        if subcategory_id:
            themes = themes.filter(subcategory_id=subcategory_id)
        elif category_id:
            themes = themes.filter(category_id=category_id, subcategory__isnull=True)

        if premium_only == "true":
            themes = themes.filter(premium=True)

        try:
            skip = int(request.query_params.get("skip", 0))
            limit = int(request.query_params.get("limit", 20))
        except ValueError:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "skip and limit must be integers"
                },
                status=422
            )

        if skip < 0 or limit < 1 or limit > 100:
            return Response(
                {
                    "status": 422,
                    "data": None,
                    "message": "skip must be positive and limit must be between 1 and 100"
                },
                status=422
            )

        total = themes.count()
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
        wallpaper_data = {
                    "id": str(theme.wallpaper.id),
                    "name": theme.wallpaper.name,
                    "preview_url": theme.wallpaper.preview_url,
                    "image_url": theme.wallpaper.image_url,
                }
        icon_items = []
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

        


        