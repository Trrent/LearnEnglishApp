from rest_framework import generics, viewsets
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework import authentication, permissions

from django.utils.text import slugify


from .models import Serial, Season, Episode
from .serializers import SerialSerializer, SeasonSerializer, EpisodeSerializer, SerialListSerializer, \
    SeasonListSerializer


def get_object(model: [Serial, Season, Episode], **kwargs) -> [Serial, Season, Episode]:
    try:
        multi_filter = ' '.join([kwargs[field] for field in kwargs])
        slug = slugify(multi_filter)
        return model.objects.get(slug=slug)
    except model.DoesNotExist:
        return


class FileUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.FILES['file']
        # do some stuff with uploaded file
        return Response(status=204)


class EpisodeDetailView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, **kwargs):
        episode = get_object(Episode, **kwargs)
        if episode:
            serializer = EpisodeSerializer(episode)
            return Response(serializer.data)
        return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, **kwargs):
        episode = get_object(Episode, **kwargs)
        if episode:
            serializer = EpisodeSerializer(episode, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, **kwargs):
        episode = get_object(Episode, **kwargs)
        if episode:
            episode.delete()
            return Response({'msg': 'content delete successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)


class SeasonDetailView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, **kwargs):
        season = get_object(Season, **kwargs)
        if season:
            serializer = SeasonSerializer(season)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        season = get_object(Season, **kwargs)
        request.data['season'] = season.id
        if not request.data.get('content'):
            request.data['content'] = {}
        episode = EpisodeSerializer(data=request.data, context={'request': request})
        if episode.is_valid():
            episode.save()
            return Response(episode.data, status=status.HTTP_200_OK)
        return Response(episode.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, **kwargs):
        season = get_object(Season, **kwargs)
        if season:
            serializer = SeasonSerializer(season, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, **kwargs):
        season = get_object(Season, **kwargs)
        if season:
            season.delete()
            return Response({'msg': 'content delete successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)


class SerialListView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, **kwargs):
        serials = Serial.objects.all()
        serializer = SerialListSerializer(serials)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        serial = SerialSerializer(data=request.data, context={'data': request.data})
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=status.HTTP_200_OK)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, **kwargs):
        serial = get_object(Serial, **kwargs)
        if serial:
            serializer = SerialSerializer(serial, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, **kwargs):
        serial = get_object(Serial, **kwargs)
        if serial:
            serial.delete()
            return Response({'msg': 'content delete successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)



class SerialDetailView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, **kwargs):
        serial = get_object(Serial, **kwargs)
        if serial:
            serializer = SerialSerializer(serial)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, **kwargs):
        serial = get_object(Serial, **kwargs)
        request.data['serial'] = serial.id
        if not request.data.get('episodes'):
            request.data['episodes'] = []
        season = SeasonSerializer(data=request.data, context={'data': request.data})
        if season.is_valid():
            season.save()
            return Response(season.data, status=status.HTTP_200_OK)
        return Response(season.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, **kwargs):
        serial = get_object(Serial, **kwargs)
        if serial:
            serializer = SerialSerializer(serial, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, **kwargs):
        serial = get_object(Serial, **kwargs)
        if serial:
            serial.delete()
            return Response({'msg': 'content delete successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)
