from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Serial, Season, Episode, ItemBase, IText, IVideo, IQuiz, Content


class ItemBaseSerializer(serializers.Serializer):
    class Meta:
        model = ItemBase
        abstract = True
        fields = ['id']


class EpisodeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ('id', 'title')


class EpisodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Episode
        fields = ('id', 'title', 'season')


class SeasonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ('id', 'title', 'slug', 'created')


class SeasonSerializer(serializers.ModelSerializer):
    episodes = EpisodeListSerializer(many=True, allow_null=True)

    def create(self, validated_data):
        episodes = validated_data.pop('episodes', [])
        season = Season.objects.create(**validated_data)
        for episode_data in episodes:
            episode_data['season'] = season
            Episode.objects.create(**episode_data)
        return season

    class Meta:
        model = Season
        fields = ('id', 'serial', 'title', 'slug', 'created', 'episodes')


class SerialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serial
        fields = ('id', 'title', 'slug')


class SerialSerializer(serializers.ModelSerializer):
    seasons = SeasonListSerializer(many=True, allow_null=True)

    class Meta:
        model = Serial
        fields = ('id', 'title', 'slug', 'seasons')
