"""Admin panel for our Watchlist models"""

from django.contrib import admin

from watchlist.models import (
    StreamPlatform,
    WatchList,
    Review,
)


class StreamPlatformAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "uid",
        "name",
        "website",
        "status",
    )


class WatchListAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "uid",
        "title",
        "story_line",
        "status",
        "created_at",
    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "uid",
        "watchlist",
        "rating",
        "status",
        "created_at",
    )


admin.site.register(StreamPlatform, StreamPlatformAdmin)

admin.site.register(WatchList, WatchListAdmin)

admin.site.register(Review, ReviewAdmin)
