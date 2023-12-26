from django.contrib import admin

from .models import Course, Season, Episode


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


class EpisodeInline(admin.StackedInline):
    model = Episode


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['slug', 'created']
    list_filter = ['created', 'course']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [EpisodeInline]