from rest_framework import serializers
from .models import Serial, Season, Episode, ItemBase, IText, IVideo, IQuiz


class ItemBaseSerializer(serializers.Serializer):

    class Meta:
        model = ItemBase
        abstract = True
        fields = ['id']


class ITextSerializer(ItemBaseSerializer, serializers.ModelSerializer):
    class Meta:
        model = IText
        fields = ItemBaseSerializer.Meta.fields + ['rus', 'eng']


class EpisodeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Episode
        fields = ['id', 'title', 'slug']


class EpisodeSerializer(serializers.ModelSerializer):
    season = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )

    def create(self, validated_data):
        return self

    class Meta:
        model = Season
        fields = ['id', 'title', 'slug', 'season']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['serial'] = self.instance.season.serial.title
        data['content'] = {}
        for content in self.instance.contents.all():
            if isinstance(content.item, IText):
                data['content']['itext'] = data['content'].get('itext', []) + [ITextSerializer(content.item).data]
            elif isinstance(content.item, IVideo):
                data['content']['ivideo'] = data['content'].get('ivideo', []) + [ITextSerializer(content.item).data]
            elif isinstance(content.item, IQuiz):
                data['content']['iquiz'] = data['content'].get('iquiz', []) + [ITextSerializer(content.item).data]
        return data


class SeasonListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Season
        fields = ['id', 'title', 'slug']


class SeasonSerializer(serializers.ModelSerializer):
    serial = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )
    episodes = EpisodeListSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Season
        fields = ['id', 'title', 'serial', 'slug', 'episodes']


class SerialListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Serial
        fields = ['id', 'title', 'slug']


class SerialSerializer(serializers.ModelSerializer):
    seasons = SeasonListSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Serial
        fields = ['id', 'title', 'slug', 'seasons']
