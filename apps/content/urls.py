from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import SerialDetailView, SerialListView, EpisodeDetailView, SeasonDetailView, FileUploadView

# router = DefaultRouter()
# router.register(r'serials', SerialDetailView, basename='posts')
# router.register(r'videos', VideoViewSet, basename='videos')
# router.register(r'files', FileViewSet, basename='files')

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='upload_file'),

    path('serials/', SerialListView.as_view(), name='serial_list'),
    path('serials/<slug>/', SerialDetailView.as_view(), name='serial_detail'),
    path('serials/<serial_slug>/<season_slug>/', SeasonDetailView.as_view(), name='season_detail'),
    path('serials/<serial_slug>/<season_slug>/<episode_slug>/', EpisodeDetailView.as_view(), name='episode_detail'),
]

# urlpatterns += router.urls
