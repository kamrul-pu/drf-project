from django.urls import reverse
from rest_framework import serializers

from watchlist.models import WatchList, StreamPlatform, Review

from common.choices import Status


def name_length(value):
    if len(value) < 5:
        raise serializers.ValidationError("Name must be at least 5 character")


# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(
#         read_only=True,
#     )
#     uid = serializers.UUIDField(
#         read_only=True,
#     )
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     status = serializers.CharField()

#     # def validate_name(self, value):
#     # if len(value) < 5:
#     #     raise serializers.ValidationError("Name must be at least 5 character")
#     # return value

#     def validate(self, attrs):
#         if attrs["name"] == attrs["description"]:
#             raise serializers.ValidationError("name and desciption cant be same")
#         return attrs

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get("name", instance.name)
#         instance.description = validated_data.get("description", instance.description)
#         instance.status = validated_data.get("status", instance.status)
#         instance.save()
#         return instance


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "id",
            "uid",
            "watchlist",
            "rating",
            "description",
        )
        read_only_fields = (
            "id",
            "uid",
            "watchlist",
        )


class WatchListSerializer(serializers.ModelSerializer):
    # link = serializers.SerializerMethodField()

    # def get_link(self, obj):
    #     request = self.context.get("request")
    #     return request.build_absolute_uri(reverse("movie-detail", args=[obj.id]))
    # name_length = serializers.SerializerMethodField()

    # def get_name_length(self, obj):
    #     return len(obj.name)
    watchlist_review = ReviewSerializer(
        many=True,
        read_only=True,
    )
    platform_name = serializers.CharField(
        source="platform.name",
        read_only=True,
    )

    class Meta:
        model = WatchList
        fields = (
            "id",
            "uid",
            "title",
            "story_line",
            "description",
            "status",
            "platform",
            "platform_name",
            "watchlist_review",
            "number_of_rating",
            "avg_rating",
            # "link",
            # "name_length",
        )
        read_only_fields = (
            "id",
            "uid",
        )

    # def validate_name(self, value):
    #     if len(value) < 5:
    #         raise serializers.ValidationError("Name must be at least 5 character")
    #     return value

    # def validate(self, attrs):
    #     if attrs["name"] == attrs["description"]:
    #         raise serializers.ValidationError("name and desciption cant be same")
    #     return attrs


class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    # watchlist = WatchListSerializer(
    #     many=True,
    #     read_only=True,
    # )
    # watchlist = serializers.StringRelatedField(many=True, read_only=True)
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    watchlist = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="movie-detail"
    )

    class Meta:
        model = StreamPlatform
        fields = (
            "id",
            "uid",
            "name",
            "about",
            "website",
            "watchlist",
        )
        read_only_fields = (
            "id",
            "uid",
        )
