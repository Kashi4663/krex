from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.forms import ModelForm
from django.contrib.auth import authenticate, login, logout
from .models import Movie, Watchlist, TvShows, Episode


# ==========================================================
# 🔐 ADMIN PROTECTION (UPDATED & SECURE)
# ==========================================================

def admin_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_superuser
    )(view_func)


# ==========================================================
# 🏠 HOME
# ==========================================================

@login_required
def home(request):
    return render(request, 'index.html')


# ==========================================================
# 📄 STATIC PAGES
# ==========================================================

def about(request):
    return render(request, 'aboutus.html')


def contact(request):
    return render(request, 'contactus.html')


# ==========================================================
# 🎬 MOVIES PAGE
# ==========================================================

def movies(request):
    trending_movies = Movie.objects.filter(is_trending=True)
    hindi_movies = Movie.objects.filter(is_hindi=True)
    english_movies = Movie.objects.filter(is_english=True)
    top_movies = Movie.objects.filter(
        top_rank__isnull=False
    ).order_by('top_rank')[:10]

    return render(request, 'aboutus.html', {
        'trending_movies': trending_movies,
        'hindi_movies': hindi_movies,
        'english_movies': english_movies,
        'top_movies': top_movies
    })


# ==========================================================
# 📺 TV SHOWS PAGE
# ==========================================================

def tv_shows(request):
    trending_shows = TvShows.objects.filter(is_trending=True)
    hindi_shows = TvShows.objects.filter(is_hindi=True)
    english_shows = TvShows.objects.filter(is_english=True)
    top_shows = TvShows.objects.filter(
        top_rank__isnull=False
    ).order_by('top_rank')[:10]

    return render(request, 'tvshows.html', {
        'trending_shows': trending_shows,
        'hindi_shows': hindi_shows,
        'english_shows': english_shows,
        'top_shows': top_shows
    })


# ==========================================================
# 🎥 MOVIE DETAIL
# ==========================================================

def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    related_movies = Movie.objects.exclude(id=id).order_by('-created_at')[:10]

    in_watchlist = False
    if request.user.is_authenticated:
        in_watchlist = Watchlist.objects.filter(
            user=request.user,
            movie=movie
        ).exists()

    return render(request, 'movie_detail.html', {
        'movie': movie,
        'related_movies': related_movies,
        'in_watchlist': in_watchlist
    })


# ==========================================================
# 📺 SHOW DETAIL
# ==========================================================

def shows_detail(request, id):
    show = get_object_or_404(
        TvShows.objects.prefetch_related('episodes'),
        id=id
    )

    related_shows = TvShows.objects.exclude(id=id).order_by('-created_at')[:10]

    in_watchlist = False
    if request.user.is_authenticated:
        in_watchlist = Watchlist.objects.filter(
            user=request.user,
            tvshow=show
        ).exists()

    return render(request, 'shows_details.html', {
        'show': show,
        'related_shows': related_shows,
        'in_watchlist': in_watchlist
    })


# ==========================================================
# 🎞 EPISODE DETAIL
# ==========================================================

def episode_detail(request, id):
    episode = get_object_or_404(
        Episode.objects.select_related('tvshow'),
        id=id
    )

    show = episode.tvshow

    related_episodes = Episode.objects.filter(
        tvshow=show
    ).exclude(id=id)

    related_shows = TvShows.objects.exclude(id=show.id).order_by('-created_at')[:10]

    in_watchlist = False
    if request.user.is_authenticated:
        in_watchlist = Watchlist.objects.filter(
            user=request.user,
            tvshow=show
        ).exists()

    return render(request, 'episode_detail.html', {
        'episode': episode,
        'show': show,
        'related_episodes': related_episodes,
        'related_shows': related_shows,
        'in_watchlist': in_watchlist
    })


# ==========================================================
# ▶ WATCH
# ==========================================================

def watch_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    return render(request, "watch_movie.html", {"movie": movie})


def watch_episode(request, id):
    episode = get_object_or_404(
        Episode.objects.select_related('tvshow'),
        id=id
    )
    return render(request, "watch_episode.html", {
        "episode": episode,
        "show": episode.tvshow
    })


# ==========================================================
# ⭐ WATCHLIST
# ==========================================================

@login_required
def toggle_watchlist(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    watch_item, created = Watchlist.objects.get_or_create(
        user=request.user,
        movie=movie
    )

    if not created:
        watch_item.delete()

    return redirect('movie_detail', id=movie.id)


@login_required
def toggle_tvshow_watchlist(request, show_id):
    show = get_object_or_404(TvShows, id=show_id)

    watch_item, created = Watchlist.objects.get_or_create(
        user=request.user,
        tvshow=show
    )

    if not created:
        watch_item.delete()

    return redirect(request.META.get('HTTP_REFERER', 'index'))


@login_required
def watchlist_view(request):
    watchlist_items = Watchlist.objects.filter(
        user=request.user
    ).order_by('-added_on')

    return render(request, 'watchlist.html', {
        'watchlist_movies': watchlist_items
    })


# ==========================================================
# 🔎 LIVE SEARCH
# ==========================================================

def live_search(request):
    query = request.GET.get('q')
    results = []

    if query:
        movies = Movie.objects.filter(
            title__icontains=query
        )[:8]

        shows = TvShows.objects.filter(
            title__icontains=query
        )[:8]

        for movie in movies:
            results.append({
                'id': movie.id,
                'title': movie.title,
                'poster': movie.poster.url if movie.poster else '',
                'type': 'movie'
            })

        for show in shows:
            results.append({
                'id': show.id,
                'title': show.title,
                'poster': show.poster.url if show.poster else '',
                'type': 'show'
            })

    return JsonResponse(results, safe=False)


# ==========================================================
# 🛠 CUSTOM ADMIN PANEL (SUPERUSER ONLY)
# ==========================================================

@admin_required
def admin_dashboard(request):
    return render(request, 'admin_panel/dashboard.html', {
        'total_movies': Movie.objects.count(),
        'total_shows': TvShows.objects.count(),
        'total_episodes': Episode.objects.count(),
    })


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'


class TvShowsForm(ModelForm):
    class Meta:
        model = TvShows
        fields = '__all__'


class EpisodeForm(ModelForm):
    class Meta:
        model = Episode
        fields = '__all__'


@admin_required
def admin_movies(request):
    movies = Movie.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/movies_list.html', {'movies': movies})


@admin_required
def add_movie(request):
    form = MovieForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('admin_movies')
    return render(request, 'admin_panel/add_movie.html', {'form': form})


@admin_required
def admin_shows(request):
    shows = TvShows.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/shows_list.html', {'shows': shows})


@admin_required
def add_show(request):
    form = TvShowsForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('admin_shows')
    return render(request, 'admin_panel/add_show.html', {'form': form})


@admin_required
def add_episode(request):
    form = EpisodeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('admin_shows')
    return render(request, 'admin_panel/add_episode.html', {'form': form})


# ==========================================================
# 🔑 AUTH SYSTEM
# ==========================================================

def select_role(request):
    return render(request, 'select_role.html')


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=email, password=password)

        if user is not None:

            # If admin selected but user is not superuser
            if role == "admin" and not user.is_superuser:
                return render(request, 'login.html', {
                    'error': "You are not authorized as admin."
                })

            login(request, user)
            return redirect('index')

        return render(request, 'login.html', {
            'error': "Invalid credentials"
        })

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('select_role')