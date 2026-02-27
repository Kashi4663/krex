from django.contrib import admin
from .models import Movie, TvShows, Episode


# ================= MOVIE ADMIN =================

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'release_year',
        'language',
        'is_trending',
        'is_hindi',
        'is_english',
        'top_rank'
    )
    list_filter = ('language', 'is_trending', 'is_hindi', 'is_english')
    search_fields = ('title',)
    ordering = ('-created_at',)


# ================= EPISODE INLINE =================

class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1


# ================= TV SHOW ADMIN =================

@admin.register(TvShows)
class TvShowsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'release_year',
        'language',
        'is_trending',
        'is_hindi',
        'is_english',
        'top_rank'
    )
    list_filter = ('language', 'is_trending', 'is_hindi', 'is_english')
    search_fields = ('title',)
    ordering = ('-created_at',)
    inlines = [EpisodeInline]


# ================= EPISODE ADMIN =================

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('tvshow', 'season', 'episode_number', 'title')
    list_filter = ('tvshow', 'season')
    search_fields = ('title',)