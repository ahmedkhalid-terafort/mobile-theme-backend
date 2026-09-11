from django.urls import path

from .views import (ArtworkCategoryListView, ArtworkSubCategoryListView, ArtworkListView, ArtworkDetailView,
                    KeyboardCategoryListView, KeyboardSubCategoryListView, KeyboardListView, KeyboardDetailView,
                    WallpaperCategoryListView, WallpaperSubCategoryListView, WallpaperListView, WallpaperDetailView,
                    ThemeCategoryListView, ThemeSubcategoryListView, ThemeListView, ThemeDetailView,
                    DiyImageListView, DiyImageDetailView, DiyFontListView, DiyFontDetailView, DiyEffectListView, DiyEffectDetailView, DiyKeyListView, DiyKeyDetailView, DiySoundListView, DiySoundDetailView)


app_name = "catalog"

urlpatterns = [
    path(
        "artwork/categories",
        ArtworkCategoryListView.as_view(),
        name="artwork-category-list",
    ),
    path(
         "artwork/categories/<uuid:category_id>/subcategories",
         ArtworkSubCategoryListView.as_view()
    ),
    path(
    "artwork",
    ArtworkListView.as_view(),
    ),
    path(
        "artwork/<uuid:artwork_id>",
        ArtworkDetailView.as_view(),
        name="artwork-detail"
    ),
    path("keyboard/categories", KeyboardCategoryListView.as_view(), name="keyboard-category-list"),

    path("keyboard/categories/<uuid:category_id>/subcategories", KeyboardSubCategoryListView.as_view()),

    path("keyboard", KeyboardListView.as_view()),

    path("keyboard/<uuid:keyboard_id>", KeyboardDetailView.as_view()),

    path("wallpaper/categories", WallpaperCategoryListView.as_view(), name="wallpaper-category-list"),

    path("wallpaper/categories/<uuid:category_id>/subcategories", WallpaperSubCategoryListView.as_view()),

    path("wallpaper", WallpaperListView.as_view()),

    path("wallpaper/<uuid:wallpaper_id>", WallpaperDetailView.as_view()),

    path(
        "theme/categories",
        ThemeCategoryListView.as_view(),
        name="theme-category-list",
    ),
    path(
        "theme/categories/<uuid:category_id>/subcategories", 
        ThemeSubcategoryListView.as_view(), 
        name="theme-subcategory-list",
    ),
    path(
        "theme",
        ThemeListView.as_view(),
        name="theme-list",
    ),
    path(
        "theme/<uuid:theme_id>",
        ThemeDetailView.as_view()
    ),

    path(
        "diy/images",
        DiyImageListView.as_view()
    ),

    path(
        "diy/images/<uuid:image_id>",
        DiyImageDetailView.as_view(),
        name="diy-image-detail",
    ),

    path(
        "diy/fonts",
        DiyFontListView.as_view()
    ),
    path(
        "diy/fonts/<uuid:font_id>",
        DiyFontDetailView.as_view(),
        name="diy-font-detail"
    ),

    path(
        "diy/effects",
        DiyEffectListView.as_view()
    ),

    path(
        "diy/effects/<uuid:effect_id>",
        DiyEffectDetailView.as_view(),
        name="diy-effect-detail"
    ),

    path(
        "diy/keys",
        DiyKeyListView.as_view()
    ),

    path(
        "diy/keys/<uuid:key_id>",
        DiyKeyDetailView.as_view(),
        name="diy-key-detail"
    ),

    path(
        "diy/sounds",
        DiySoundListView.as_view()
    ),

    path(
        "diy/sounds/<uuid:sound_id>",
        DiySoundDetailView.as_view(),
        name="diy-sound-detail"
    )

]
