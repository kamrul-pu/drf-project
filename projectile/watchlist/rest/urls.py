from django.urls import path

from watchlist.rest.views import (
    movie_list,
    movie_detail,
    WatchlistList,
    WatchlistDetail,
    StramPlatformList,
    StramPlatformDetail,
    ReviewList,
    ReviewDetail,
    UserReview,
    WatchListG,
)

urlpatterns = [
    path("/stream-platform", StramPlatformList.as_view(), name="stream-platform"),
    path(
        "/stream-platform/<int:pk>",
        StramPlatformDetail.as_view(),
        name="stream-platform-detail",
    ),
    path("", WatchlistList.as_view(), name="movie-list"),
    path("/<int:pk>", WatchlistDetail.as_view(), name="movie-detail"),
    path("/<int:watchlist_id>/reviews", ReviewList.as_view(), name="review-list"),
    path(
        "/<int:watchlist_id>/reviews/<int:pk>",
        ReviewDetail.as_view(),
        name="review-detail",
    ),
    path("/reviews/<str:user>", UserReview.as_view(), name="user-review"),
    path("/test", WatchListG.as_view(), name="watchlist-test"),
]
