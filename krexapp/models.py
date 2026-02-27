from django.db import models
from django.contrib.auth.models import User


# ================= MOVIE =================

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    poster = models.ImageField(upload_to='posters/')
    banner = models.ImageField(upload_to='banners/', null=True, blank=True)

    video = models.FileField(upload_to='videos/', null=True, blank=True)
    trailer = models.FileField(upload_to='trailers/', null=True, blank=True)

    release_year = models.IntegerField()
    language = models.CharField(max_length=50)

    is_trending = models.BooleanField(default=False)
    is_hindi = models.BooleanField(default=False)
    is_english = models.BooleanField(default=False)

    top_rank = models.IntegerField(null=True, blank=True)

    watch_link = models.URLField(blank=True, null=True)
    more_info_link = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# ================= TV SHOW =================

class TvShows(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    poster = models.ImageField(upload_to='posters/')
    banner = models.ImageField(upload_to='banners/', null=True, blank=True)

    video = models.FileField(upload_to='videos/', null=True, blank=True)
    trailer = models.FileField(upload_to='trailers/', null=True, blank=True)

    release_year = models.IntegerField()
    language = models.CharField(max_length=50)

    is_trending = models.BooleanField(default=False)
    is_hindi = models.BooleanField(default=False)
    is_english = models.BooleanField(default=False)

    top_rank = models.IntegerField(null=True, blank=True)

    watch_link = models.URLField(blank=True, null=True)
    more_info_link = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# ================= EPISODE =================

class Episode(models.Model):
    tvshow = models.ForeignKey(
        TvShows,
        on_delete=models.CASCADE,
        related_name='episodes'
    )

    season = models.IntegerField(default=1)
    episode_number = models.IntegerField()

    title = models.CharField(max_length=200)
    description = models.TextField()

    video = models.FileField(upload_to='episodes/')
    thumbnail = models.ImageField(upload_to='episode_thumbnails/', null=True, blank=True)

    class Meta:
        ordering = ['season', 'episode_number']
        unique_together = ('tvshow', 'season', 'episode_number')  # 🔥 Prevent duplicate episodes

    def __str__(self):
        return f"{self.tvshow.title} - S{self.season}E{self.episode_number}"


# ================= WATCHLIST =================

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    tvshow = models.ForeignKey(TvShows, on_delete=models.CASCADE, null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'movie'],
                name='unique_user_movie'
            ),
            models.UniqueConstraint(
                fields=['user', 'tvshow'],
                name='unique_user_tvshow'
            ),
        ]

    def __str__(self):
        if self.movie:
            return f"{self.user.username} - {self.movie.title}"
        if self.tvshow:
            return f"{self.user.username} - {self.tvshow.title}"