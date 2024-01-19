from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework import authentication, permissions

from django.utils.text import slugify


from .models import Serial, Season, Episode
from .serializers import SerialSerializer, SerialListSerializer, SeasonSerializer, EpisodeSerializer


def get_object(model: [Serial, Season, Episode], slug: str) -> [Serial, Season, Episode]:
    try:
        return model.objects.get(slug=slug)
    except model.DoesNotExist:
        return


class MultipleFieldLookupMixin:
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        multi_filter = ' '.join([self.kwargs[field] for field in self.lookup_fields])
        slug = slugify(multi_filter)
        obj = get_object_or_404(queryset, slug=slug)
        self.check_object_permissions(self.request, obj)
        return obj


class SerialListView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = Serial.objects.all()
        serializer = SerialListSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        # print(request.data)
        # seasons = request.data.pop('seasons')
        # episodes = seasons.pop('episodes')
        serializer = SerialListSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SerialDetailView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug):
        serial = get_object(Serial, slug)
        if serial:
            serializer = SerialSerializer(serial)
            return Response(serializer.data)
        return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)

    # def post(self, request, slug):
    #     serial = get_object(Serial, slug)
    #     request.data['serial'] = serial
    #     print(request.data)
    #     serializer = SeasonSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, slug):
        serial = get_object(Serial, slug)
        if serial:
            serializer = SerialSerializer(serial, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, slug):
        serial = get_object(Serial, slug)
        if serial:
            serial.delete()
            return Response({'msg': 'content delete successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)


class SeasonDetailView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, **kwargs):
        multi_filter = ' '.join([kwargs[field] for field in kwargs])
        slug = slugify(multi_filter)
        season = get_object(Season, slug)
        if season:
            serializer = SeasonSerializer(season)
            return Response(serializer.data)
        return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)

    # def post(self, request):
    #     serializer = SeasonSerializer(data=request.data, many=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, **kwargs):
        multi_filter = ' '.join([kwargs[field] for field in kwargs])
        slug = slugify(multi_filter)
        season = get_object(Season, slug)
        if season:
            serializer = SeasonSerializer(season, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, **kwargs):
        multi_filter = ' '.join([kwargs[field] for field in kwargs])
        slug = slugify(multi_filter)
        season = get_object(Episode, slug)
        if season:
            season.delete()
            return Response({'msg': 'content delete successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)


class EpisodeDetailView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, **kwargs):
        multi_filter = ' '.join([kwargs[field] for field in kwargs])
        slug = slugify(multi_filter)
        episode = get_object(Episode, slug)
        if episode:
            serializer = EpisodeSerializer(episode)
            return Response(serializer.data)
        return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, **kwargs):
        multi_filter = ' '.join([kwargs[field] for field in kwargs])
        slug = slugify(multi_filter)
        episode = get_object(Episode, slug)
        if episode:
            serializer = EpisodeSerializer(episode, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, **kwargs):
        multi_filter = ' '.join([kwargs[field] for field in kwargs])
        slug = slugify(multi_filter)
        episode = get_object(Episode, slug)
        if episode:
            episode.delete()
            return Response({'msg': 'content delete successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)