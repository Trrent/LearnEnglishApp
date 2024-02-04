from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType


from .models import Serial, Season, Episode, IText, IVideo, IQuiz, Content


class ITextSerializer(serializers.ModelSerializer):
    class Meta:
        model = IText
        fields = ['id', 'rus', 'eng']


class EpisodeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ('id', 'title', 'slug')


class EpisodeSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        content = self.context['data'].pop('content', {})
        episode = Episode.objects.create(**validated_data)
        for content_type in content:
            for content_data in content[content_type]:
                if content_type == 'itext':
                    item = IText.objects.create(**content_data)
                elif content_type == 'ivideo':
                    item = IVideo.objects.create(**content_data)
                elif content_type == 'iquiz':
                    item = IQuiz.objects.create(**content_data)
                Content.objects.create(
                        episode=episode,
                        content_type=ContentType.objects.get(model=content_type),
                        object_id=item.id
                )
        return episode

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['season'] = self.instance.season.title
        data['serial'] = self.instance.season.serial.title
        data['content'] = {}
        for content in self.instance.content.all():
            if isinstance(content.item, IText):
                data['content']['itext'] = data['content'].get('itext', []) + [ITextSerializer(content.item).data]
            elif isinstance(content.item, IVideo):
                data['content']['ivideo'] = data['content'].get('ivideo', []) + [ITextSerializer(content.item).data]
            elif isinstance(content.item, IQuiz):
                data['content']['iquiz'] = data['content'].get('iquiz', []) + [ITextSerializer(content.item).data]
        return data

    class Meta:
        model = Episode
        fields = ('id', 'title', 'slug', 'season')


class SeasonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ('id', 'title', 'slug')


class SeasonSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        episodes = self.context['data'].pop('episodes', [])
        season = Season.objects.create(**validated_data)
        for episode_data in episodes:
            episode_data['season'] = season.id
            episode = EpisodeSerializer(data=episode_data, context={'data': episode_data})
            if episode.is_valid(raise_exception=True):
                episode.save()
        return season

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['serial'] = self.instance.serial.title
        if self.instance.episodes.all():
            data['episodes'] = EpisodeListSerializer(self.instance.episodes.all(), many=True).data
        return data

    class Meta:
        model = Season
        fields = ('id', 'title', 'slug', 'serial')


class SerialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serial
        fields = ('id', 'title', 'slug')


class SerialSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.instance.seasons.all():
            data['seasons'] = SeasonListSerializer(self.instance.seasons.all(), many=True).data
        return data

    class Meta:
        model = Serial
        fields = ('id', 'title', 'slug')
