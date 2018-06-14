from rest_framework import serializers
from .models import MovieModel, MovieReview

from django.contrib.auth import (authenticate, get_user_model, login, logout)

UserModel = get_user_model()


class MovieReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieReview
        fields = [
            'review_title',
            'review',
            'rating'
        ]


class MoviePostSerializer(serializers.ModelSerializer):
    reviews = MovieReviewSerializer(read_only=True, many=True)

    class Meta:
        model = MovieModel
        fields = [
            'pk',
            'title',
            'release_date',
            'movie_rating',
            'trailer',
            'synopsis',
            'image',
            'reviews'
        ]
        read_only_fields = ["pk"]

    def validate_title(self, value):
        qs = MovieModel.objects.filter(title__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.count() >= 1:
            raise serializers.ValidationError("Movie with same name already exist")
        return value
