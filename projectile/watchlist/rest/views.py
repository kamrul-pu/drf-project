"""Views for WatchList"""
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from watchlist.permissions import AdminOrReadOnly, ReviewPermissionOrReadOnly
from watchlist.rest.serializers import (
    WatchListSerializer,
    StreamPlatformSerializer,
    ReviewSerializer,
)
from watchlist.models import WatchList, StreamPlatform, Review
from watchlist.pagination import WatchlistPagination, ReviewListPagination
from watchlist.throtlling import ReviewCreateThrottle, ReviewListThrottle


@api_view(["GET", "POST"])
def movie_list(request):
    if request.method == "GET":
        watchlists = WatchList.objects.filter()
        serializer = WatchListSerializer(watchlists, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "POST":
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def movie_detail(request, pk):
    obj = get_object_or_404(WatchList, pk=pk)
    if request.method == "GET":
        WatchList = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(WatchList)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        WatchList = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(instance=WatchList, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"message": "Method not allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif request.method == "PATCH":
        WatchList = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(
            instance=WatchList, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"message": "Method not allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif request.method == "DELETE":
        WatchList = WatchList.objects.get(pk=pk)
        WatchList.delete()
        return Response(
            {"message": "Deleted Successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    return Response(
        {"message": "Method not allowed"},
        status=status.HTTP_400_BAD_REQUEST,
    )


class StramPlatformList(ListCreateAPIView):
    serializer_class = StreamPlatformSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = StreamPlatform.objects.filter().prefetch_related(
        "watchlist",
    )


class StramPlatformDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = StreamPlatformSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = StreamPlatform.objects.filter()


class WatchlistList(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = WatchListSerializer
    # pagination_class = WatchlistPagination
    # def _get(self, pk):
    #     obj = get_object_or_404(WatchList, pk=pk)
    #     return obj

    def get(self, request, format=None):
        watchlists = (
            WatchList.objects.filter()
            .only(
                "id",
                "uid",
                "title",
                "story_line",
                "description",
                "status",
                "platform",
                "platform__name",
                "number_of_rating",
                "avg_rating",
            )
            .select_related("platform")
            .prefetch_related("watchlist_review")
        )
        name = request.query_params.get("name", None)
        if name:
            watchlists = watchlists.filter(
                title__icontains=name,
            )
        serializer = self.serializer_class(
            watchlists, many=True, context={"request": request}
        )
        return Response(
            {"watchlists": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchlistDetail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = WatchListSerializer

    def _get(self, pk):
        return get_object_or_404(WatchList, pk=pk)

    def get(self, request, pk):
        watchlist = self._get(pk)
        serializer = self.serializer_class(watchlist, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, **kwargs):
        watchlist = self._get(pk)
        serializer = WatchListSerializer(instance=watchlist, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"message": "Method not allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, pk):
        watchlist = self._get(pk)
        serializer = WatchListSerializer(
            instance=watchlist, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"message": "Method not allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        watchlist = get_object_or_404(WatchList, pk=pk)
        watchlist.delete()
        return Response(
            {"message": "Deleted Successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ReviewList(ListCreateAPIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewCreateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user__full_name", "rating"]
    pagination_class = ReviewListPagination

    def get_queryset(self):
        watchlist_id = self.kwargs.get("watchlist_id", None)
        queryset = Review.objects.filter(watchlist__id=watchlist_id).select_related(
            "user"
        )
        return queryset

    def perform_create(self, serializer):
        watchlist_id = watchlist_id = self.kwargs.get("watchlist_id", None)
        watchlist = WatchList.objects.get(pk=watchlist_id)
        user = self.request.user
        review = Review.objects.filter(watchlist=watchlist, user=user)
        if review.exists():
            raise ValidationError("You already have review for this movie")

        rating = serializer.validated_data["rating"]
        if watchlist.number_of_rating == 0:
            watchlist.avg_rating = rating
        else:
            watchlist.avg_rating = (watchlist.avg_rating + rating) / 2
        watchlist.number_of_rating += 1
        watchlist.save(update_fields=["avg_rating", "number_of_rating"])
        serializer.save(watchlist=watchlist, user=user)


class ReviewDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [
        ReviewPermissionOrReadOnly,
    ]
    serializer_class = ReviewSerializer
    queryset = Review.objects.filter()

    def get_queryset(self):
        queryset = self.queryset
        watchlist_id = watchlist_id = self.kwargs.get("watchlist_id", None)
        pk = self.kwargs.get("pk", None)
        return queryset.filter(watchlist_id=watchlist_id, pk=pk)


class UserReview(ListAPIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        user = self.kwargs["user"]
        if user is not None:
            return Review.objects.filter(user__full_name__icontains=user)
        return Review.objects.filter()


class WatchListG(ListAPIView):
    queryset = (
        WatchList.objects.filter()
        .select_related("platform")
        .prefetch_related("watchlist_review")
    )
    serializer_class = WatchListSerializer
    pagination_class = WatchlistPagination
    # filter is like Search exact , i mean match whole value query_params is like filterset_fields
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["title", "number_of_rating", "avg_rating", "platform__name"]
    # /api/v1/watchlist/test?title=Thor Thunder / platform__name=Netflix
    # Search
    # filter_backends = [filters.SearchFilter]
    # search_fields = ["title", "platform__name"]
    # /api/v1/watchlist/test?search=netflix
    # /api/v1/watchlist/test?search=thor

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["avg_rating"]
    # /api/v1/watchlist/test?search=netflix&ordering=-avg_rating dsc
    # /api/v1/watchlist/test?search=thor&ordering=avg_rating asc
