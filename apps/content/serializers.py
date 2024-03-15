from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType

from .models import Serial, Season, Episode, IText, IVideo, IQuiz, Content, Video


class ITextSerializer(serializers.ModelSerializer):
    class Meta:
        model = IText
        fields = ['id', 'rus', 'eng']


class VideoSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('i_video')
        return data

    class Meta:
        model = Video
        fields = ['quality', 'src', 'i_video']


class IVideoSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        video = self.context['request'].FILES.get('video', None)
        quality = self.context['request'].data.get('quality', None)

        i_video = IVideo.objects.create(**validated_data)
        video = VideoSerializer(data={
            'quality': quality,
            'src': video,
            'i_video': i_video.id,
        })
        if video.is_valid(raise_exception=True):
            video.save()
        return i_video

    def to_representation(self, instance):
        data = super().to_representation(instance)
        quality_src = []
        for video in instance.qualitySrc.all():
            quality_src.append(VideoSerializer(video).data)
        data['qualitySrc'] = quality_src
        return data

    class Meta:
        model = IVideo
        fields = ['id', 'name', 'poster', 'subtitles']


class EpisodeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ('id', 'title', 'slug')


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ('id', 'title', 'slug')

    def create(self, validated_data):
        content = self.context['data'].pop('content', {})
        validated_data['season'] = self.context['season']
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
                print(content.item)
                data['content']['ivideo'] = data['content'].get('ivideo', []) + [IVideoSerializer(content.item).data]
            elif isinstance(content.item, IQuiz):
                data['content']['iquiz'] = data['content'].get('iquiz', []) + [ITextSerializer(content.item).data]
        return data


class SeasonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ('id', 'title', 'slug')


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ('id', 'title', 'slug')

    def create(self, validated_data):
        episodes = self.context['data'].pop('episodes', [])
        validated_data['serial'] = self.context['serial']
        season = Season.objects.create(**validated_data)
        for episode_data in episodes:
            # episode_data['season'] = season.id
            episode = EpisodeSerializer(data=episode_data, context={'data': episode_data, 'season': season})
            if episode.is_valid(raise_exception=True):
                episode.save()
        return season

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['serial'] = self.instance.serial.title
        if self.instance.episodes.all():
            data['episodes'] = EpisodeListSerializer(self.instance.episodes.all(), many=True).data
        return data


class SerialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serial
        fields = ('id', 'title', 'slug')


class SerialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serial
        fields = ('id', 'title', 'slug')

    def create(self, validated_data):
        seasons = self.context['data'].pop('seasons', [])
        serial = Serial.objects.create(**validated_data)
        for season_data in seasons:
            season = SeasonSerializer(data=season_data, context={'data': season_data, 'serial': serial})
            if season.is_valid(raise_exception=True):
                season.save()
        return serial

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.instance.seasons.all():
            data['seasons'] = SeasonListSerializer(self.instance.seasons.all(), many=True).data
        return data
