from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Category, CoolFont, Keyboard
)
from.permissions import HasMobileThemeAPIKey
from .serializers import (
    CategorySerializer, SubCategorySerializer,
    CoolFontSerializer,
    KeyboardSerializer
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

