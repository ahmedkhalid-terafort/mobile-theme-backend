from django.urls import path

from .views import (ArtworkCategoryListView, ArtworkSubCategoryListView, ArtworkListView, ArtworkDetailView,
                    KeyboardCategoryListView, KeyboardSubCategoryListView, KeyboardListView, KeyboardDetailView,
                    WallpaperCategoryListView, WallpaperSubCategoryListView, WallpaperListView, WallpaperDetailView,
                    ThemeCategoryListView, ThemeSubcategoryListView, ThemeListView, ThemeDetailView,
                    DiyImageListView, DiyImageDetailView, DiyFontListView, DiyFontDetailView, DiyEffectListView, DiyEffectDetailView, DiyKeyListView, DiyKeyDetailView, DiySoundListView, DiySoundDetailView)

from .views_v2 import (
    ArtWorkCategoryListViewV2, ArtWorkSubCategoryListViewV2, ArtWorkListViewV2, ArtWorkDetailViewV2,
    KeyboardCategoryListViewV2, KeyboardSubcategoryListViewV2, KeyboardListViewV2, KeyboardDetailViewV2,
    WallpaperCategoryListViewV2, WallpaperSubcategoryListViewV2, WallpaperListViewV2, WallpaperDetailViewV2,
    ThemeCategoryListViewV2, ThemeSubcategoryListViewV2, ThemeListViewV2, ThemeDetailViewV2,
    DiyImageListViewV2, DiyImageDetailViewV2, DiyFontListViewV2, DiyFontDetailViewV2,
    DiyEffectListViewV2, DiyEffectDetailViewV2, DiyKeyListViewV2, DiyKeyDetailViewV2,
    DiySoundListViewV2, DiySoundDetailViewV2
)


app_name = "catalog"

urlpatterns = [
    # ArtWork APIs v1
    path("artwork/categories", ArtworkCategoryListView.as_view(), name="artwork-category-list"),
    path("artwork/categories/<uuid:category_id>/subcategories", ArtworkSubCategoryListView.as_view()),
    path("artwork", ArtworkListView.as_view()),
    path("artwork/<uuid:artwork_id>", ArtworkDetailView.as_view(), name="artwork-detail"),

    #ArtWork APIs v2
    path("v2/artwork/categories", ArtWorkCategoryListViewV2.as_view(), name="v2-artwork-category-list"),
    path("v2/artwork/categories/<uuid:category_id>/subcategories", ArtWorkSubCategoryListViewV2.as_view()),
    path("v2/artwork", ArtWorkListViewV2.as_view()),
    path("v2/artwork/<uuid:artwork_id>", ArtWorkDetailViewV2.as_view(), name="v2-artwork-detal"),

    # Keyboard APIs v1
    path("keyboard/categories", KeyboardCategoryListView.as_view(), name="keyboard-category-list"),
    path("keyboard/categories/<uuid:category_id>/subcategories", KeyboardSubCategoryListView.as_view()),
    path("keyboard", KeyboardListView.as_view()),
    path("keyboard/<uuid:keyboard_id>", KeyboardDetailView.as_view()),

    # Keyborad APIs v2
    path("v2/keyboard/categories", KeyboardCategoryListViewV2.as_view(), name="v2-keyboard-category-list"),
    path("v2/keyboard/categories/<uuid:category_id>/subcategories", KeyboardSubcategoryListViewV2.as_view()),
    path("v2/keyboard", KeyboardListViewV2.as_view()),
    path("v2/keyboard/<uuid:keyboard_id>", KeyboardDetailViewV2.as_view()),

    # Wallpaper APIs v1
    path("wallpaper/categories", WallpaperCategoryListView.as_view(), name="wallpaper-category-list"),
    path("wallpaper/categories/<uuid:category_id>/subcategories", WallpaperSubCategoryListView.as_view()),
    path("wallpaper", WallpaperListView.as_view()),
    path("wallpaper/<uuid:wallpaper_id>", WallpaperDetailView.as_view()),

    # Wallpaper APIs v2
    path("v2/wallpaper/categories", WallpaperCategoryListViewV2.as_view(), name="v2-wallpaper-category-list"),
    path("v2/wallpaper/categories/<uuid:category_id>/subcategories", WallpaperSubcategoryListViewV2.as_view()),
    path("v2/wallpaper", WallpaperListViewV2.as_view()),
    path("v2/wallpaper/<uuid:wallpaper_id>", WallpaperDetailViewV2.as_view(), name="v2-wallpaper-detail"),

    # Theme APIs v1
    path("theme/categories", ThemeCategoryListView.as_view(), name="theme-category-list"),
    path("theme/categories/<uuid:category_id>/subcategories", ThemeSubcategoryListView.as_view(), name="theme-subcategory-list"),
    path("theme", ThemeListView.as_view(), name="theme-list"),
    path("theme/<uuid:theme_id>", ThemeDetailView.as_view()),

    # Theme APIs v2
    path("v2/theme/categories", ThemeCategoryListViewV2.as_view(), name="v2-theme-category-list"),
    path("v2/theme/categories/<uuid:category_id>/subcategories", ThemeSubcategoryListViewV2.as_view()),
    path("v2/theme", ThemeListViewV2.as_view()),
    path("v2/theme/<uuid:theme_id>", ThemeDetailViewV2.as_view(), name="v2-theme-detail"),

    #DIY APIs v1
    path("diy/images", DiyImageListView.as_view()),
    path("diy/images/<uuid:image_id>", DiyImageDetailView.as_view(), name="diy-image-detail"),
    path("diy/fonts", DiyFontListView.as_view()),
    path("diy/fonts/<uuid:font_id>", DiyFontDetailView.as_view(), name="diy-font-detail"),
    path("diy/effects", DiyEffectListView.as_view()),
    path("diy/effects/<uuid:effect_id>", DiyEffectDetailView.as_view(), name="diy-effect-detail"),
    path("diy/keys", DiyKeyListView.as_view()),
    path("diy/keys/<uuid:key_id>", DiyKeyDetailView.as_view(), name="diy-key-detail"),
    path("diy/sounds", DiySoundListView.as_view()),
    path("diy/sounds/<uuid:sound_id>", DiySoundDetailView.as_view(), name="diy-sound-detail"),

    # DIY APIs V2
    path("v2/diy/images", DiyImageListViewV2.as_view(), name="v2-diy-image-list"),
    path("v2/diy/images/<uuid:image_id>", DiyImageDetailViewV2.as_view(), name="v2-diy-image-detail"),
    path("v2/diy/fonts", DiyFontListViewV2.as_view(), name="v2-diy-font-list"),
    path("v2/diy/fonts/<uuid:font_id>", DiyFontDetailViewV2.as_view(), name="v2-diy-font-detail"),
    path("v2/diy/effects", DiyEffectListViewV2.as_view(), name="v2-diy-effect-list"),
    path("v2/diy/effects/<uuid:effect_id>", DiyEffectDetailViewV2.as_view(), name="v2-diy-effect-detail"),
    path("v2/diy/keys", DiyKeyListViewV2.as_view(), name="v2-diy-key-list"),
    path("v2/diy/keys/<uuid:key_id>", DiyKeyDetailViewV2.as_view(), name="v2-diy-key-detail"),
    path("v2/diy/sounds", DiySoundListViewV2.as_view(), name="v2-diy-sound-list"),
    path("v2/diy/sounds/<uuid:sound_id>", DiySoundDetailViewV2.as_view(), name="v2-diy-sound-detail"),

]
