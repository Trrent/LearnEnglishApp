from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework import authentication, permissions

from django.utils.text import slugify


from .models import Serial, Season, Episode
from .serializers import SerialSerializer, SeasonSerializer, EpisodeSerializer, SerialListSerializer, \
    SeasonListSerializer


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


# class SerialListView(APIView):
#     # permission_classes = [permissions.IsAuthenticated]
#
#     def get(self, request):
#         queryset = Serial.objects.all()
#         serializer = SerialListSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     # def get_serializer(self, model: [Serial, Season, Episode], serializer: [SerialSerializer, SeasonSerializer, EpisodeSerializer], data: dict) -> [SerialSerializer, SeasonSerializer, EpisodeSerializer]:
#     #     object = get_object(model, slugify(data['title']))
#     #     if not object:
#     #         object = serializer(data=data)
#     #         if not object.is_valid():
#     #             return object
#     #         object.save()
#     #     else:
#     #         object = serializer(object)
#     #     return object
#
#     def post(self, request):
#         seasons = request.data.pop('seasons', [])
#         serial_object = get_object(Serial, slugify(request.data['title']))
#         if not serial_object:
#             serial_object = SerialSerializer(data=request.data)
#             if not serial_object.is_valid():
#                 return Response(serial_object.errors, status=status.HTTP_400_BAD_REQUEST)
#             serial_object = serial_object.save()
#         else:
#             serial_object = SerialSerializer(serial_object)
#         print(serial_object)
#         for season_data in seasons:
#             episodes = season_data.pop('episodes', [])
#
#             season_object = get_object(Season, slugify(season_data['title']))
#             if not season_object:
#                 season_object = SeasonSerializer(data=season_data)
#                 if not season_object.is_valid():
#                     return Response(serial_object.errors, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 season_object = SeasonSerializer(season_object)
#             season_object.serial = serial_object.data['id']
#             season_object = season_object.save()
#             print(season_object)
#             # # season_data['serial_id'] = serial_object.data.get('id')
#             # season_object = SeasonSerializer(data=season_data)
#             # season_object.serial = serial_object.data
#             # if season_object.is_valid():
#             #     season_object.save()
#             print(season_object.data)
#     #         new_episodes = []
#     #         for episode_data in episodes:
#     #             content = episode_data.pop('content')
#     #             episode_data['season'] = season_object
#     #             episode_object = Episode(**episode_data)
#     #             new_content = []
#     #             for content_type, items in content.items():
#     #                 for obj in items:
#     #                     if content_type == 'itext':
#     #                         item_object = IText(**obj)
#     #                     elif content_type == 'ivideo':
#     #                         item_object = IVideo(**obj)
#     #                     else:
#     #                         raise ValidationError("content_type does not supported")
#     #                     Content({'episode': episode_object,
#     #                              'content_type': content_type,
#     #                              'object_id': item_object.id})
#     #     return serial_object
#
#         # serial_object = SerialSerializer(data=request.data)
#         # if serial_object.is_valid():
#         #     serial_object.save()
#         #     return Response(serial_object.data, status=status.HTTP_201_CREATED)
#         return Response(serial_object.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class SerialDetailView(APIView):
#     # permission_classes = [permissions.IsAuthenticated]
#
#     def get(self, request, slug):
#         serial = get_object(Serial, slug)
#         if serial:
#             serializer = SerialSerializer(serial)
#             return Response(serializer.data)
#         return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     def post(self, request, slug):
#         serial = get_object(Serial, slug)
#         # request.data['serial'] = serial
#         # print(request.data)
#         serializer = SeasonSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, slug):
#         serial = get_object(Serial, slug)
#         if serial:
#             serializer = SerialSerializer(serial, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     def delete(self, request, slug):
#         serial = get_object(Serial, slug)
#         if serial:
#             serial.delete()
#             return Response({'msg': 'content delete successfully'}, status=status.HTTP_204_NO_CONTENT)
#         return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)


# class SeasonDetailView(APIView):
#     # permission_classes = [permissions.IsAuthenticated]
#
#     def get(self, request, **kwargs):
#         multi_filter = ' '.join([kwargs[field] for field in kwargs])
#         slug = slugify(multi_filter)
#         season = get_object(Season, slug)
#         if season:
#             serializer = SeasonSerializer(season)
#             return Response(serializer.data)
#         return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     # def post(self, request):
#     #     serializer = SeasonSerializer(data=request.data, many=True)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, **kwargs):
#         multi_filter = ' '.join([kwargs[field] for field in kwargs])
#         slug = slugify(multi_filter)
#         season = get_object(Season, slug)
#         if season:
#             serializer = SeasonSerializer(season, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     def delete(self, request, **kwargs):
#         multi_filter = ' '.join([kwargs[field] for field in kwargs])
#         slug = slugify(multi_filter)
#         season = get_object(Episode, slug)
#         if season:
#             season.delete()
#             return Response({'msg': 'content delete successfully'}, status=status.HTTP_204_NO_CONTENT)
#         return Response({'msg': 'content not found'}, status=status.HTTP_404_NOT_FOUND)


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


class SeasonDetailView(MultipleFieldLookupMixin,
                       generics.CreateAPIView,
                       generics.RetrieveUpdateDestroyAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    lookup_fields = ['serial_slug', 'season_slug']

    # def create(self, request, *args, **kwargs):
    #     seas = self.get_object()
    #     request.data['serial'] = serial.id
    #     if not request.data.get('episodes'):
    #         request.data['episodes'] = []
    #     season = EpisodeSerializer(data=request.data)
    #     if season.is_valid():
    #         season.save()
    #         return Response(season.data, status=status.HTTP_200_OK)
    #     return Response(season.errors, status=status.HTTP_400_BAD_REQUEST)


class SerialListView(generics.ListAPIView,
                     generics.CreateAPIView,
                     generics.RetrieveUpdateDestroyAPIView):
    queryset = Serial.objects.all()
    serializer_class = SerialListSerializer


class SerialDetailView(MultipleFieldLookupMixin,
                       generics.CreateAPIView,
                       generics.RetrieveUpdateDestroyAPIView):
    queryset = Serial.objects.all()
    serializer_class = SerialSerializer
    lookup_fields = ['slug']

    def create(self, request, *args, **kwargs):
        serial = self.get_object()
        request.data['serial'] = serial.id
        if not request.data.get('episodes'):
            request.data['episodes'] = []
        season = SeasonSerializer(data=request.data)
        if season.is_valid():
            season.save()
            return Response(season.data, status=status.HTTP_200_OK)
        return Response(season.errors, status=status.HTTP_400_BAD_REQUEST)