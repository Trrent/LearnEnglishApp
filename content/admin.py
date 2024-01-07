from django.contrib import admin

from .models import Serial, Season, Episode, Content, IText, IVideo, IQuiz


@admin.register(Serial)
class SerialAdmin(admin.ModelAdmin):
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
    list_filter = ['created', 'serial']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [EpisodeInline]


class ContentInline(admin.StackedInline):
    model = Content


@admin.register(IText)
class ITextAdmin(admin.ModelAdmin):
    list_display = ['id', 'rus']
    inlines = [ContentInline]


@admin.register(IVideo)
class IVideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(IQuiz)
class IQuizAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['episode', 'item']
    # inlines = [ITextInline]
