from rest_framework import generics
from rest_framework.generics import get_object_or_404
from django.utils.text import slugify


from .models import Serial, Season, Episode
from .serializers import SerialSerializer, SerialListSerializer, SeasonSerializer, EpisodeSerializer


class MultipleFieldLookupMixin:
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        multi_filter = ' '.join([self.kwargs[field] for field in self.lookup_fields])
        slug = slugify(multi_filter)
        obj = get_object_or_404(queryset, slug=slug)
        self.check_object_permissions(self.request, obj)
        return obj


class SerialListView(generics.ListAPIView):
    queryset = Serial.objects.all()
    serializer_class = SerialListSerializer


class SerialDetailView(generics.RetrieveAPIView):
    queryset = Serial.objects.all()
    serializer_class = SerialSerializer
    lookup_field = 'slug'


class SeasonDetailView(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    lookup_fields = ['serial_slug', 'season_slug']


class EpisodeDetailView(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    lookup_fields = ['serial_slug', 'season_slug', 'episode_slug']
