from django.urls import path
from .views import SerialDetailView, SerialListView, EpisodeDetailView, SeasonDetailView

urlpatterns = [
    path('serials/', SerialListView.as_view(), name='serial_list'),
    path('serials/<slug>/', SerialDetailView.as_view(), name='serial_detail'),
    path('serials/<serial_slug>/<season_slug>/', SeasonDetailView.as_view(), name='season_detail'),
    path('serials/<serial_slug>/<season_slug>/<episode_slug>/', EpisodeDetailView.as_view(), name='episode_detail'),
]
