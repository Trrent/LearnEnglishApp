from rest_framework import serializers
from .models import Serial, Season, Episode, Content, ItemBase, IText, IVideo, IQuiz


class ItemBaseSerializer(serializers.Serializer):
    id = serializers.UUIDField()

    class Meta:
        model = ItemBase
        abstract = True
        fields = ['id']


class ITextSerializer(ItemBaseSerializer, serializers.ModelSerializer):
    class Meta:
        model = IText
        fields = ItemBaseSerializer.Meta.fields + ['rus', 'eng']


class EpisodeListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = Episode
        fields = ['id', 'title', 'slug']


class EpisodeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    season = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = Season
        fields = ['id', 'title', 'season']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['content'] = {'itext': [],
                           'ivideo': [],
                           'iquiz': []}
        for content in self.instance.contents.all():
            if isinstance(content.item, IText):
                data['content']['itext'] += [ITextSerializer(content.item).data]
            elif isinstance(content.item, IVideo):
                data['content']['ivideo'] += [ITextSerializer(content.item).data]
            elif isinstance(content.item, IQuiz):
                data['content']['iquiz'] += [ITextSerializer(content.item).data]
            else:
                raise Exception('Unexpected type of tagged object')
        return data


class SeasonListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = Season
        fields = ['id', 'title', 'slug']


class SeasonSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
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
    id = serializers.UUIDField()

    class Meta:
        model = Serial
        fields = ['id', 'title', 'slug']


class SerialSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    seasons = SeasonListSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Serial
        fields = ['id', 'title', 'slug', 'seasons']
