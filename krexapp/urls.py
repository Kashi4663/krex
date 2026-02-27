from django.urls import path
from . import views

urlpatterns = [

    # 🔥 Homepage moved to /home/
    path('home/', views.home, name='index'),

    # ================= AUTH SYSTEM =================
    path('select-role/', views.select_role, name='select_role'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ================= STATIC PAGES =================
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # ================= MOVIES =================
    path('movies/', views.movies, name='movies'),
    path('movie/<int:id>/', views.movie_detail, name='movie_detail'),
    path('watch/<int:id>/', views.watch_movie, name='watch_movie'),
    path('watchlist/<int:movie_id>/', views.toggle_watchlist, name='toggle_watchlist'),

    # ================= TV SHOWS =================
    path('tv-shows/', views.tv_shows, name='tv_shows'),
    path('show/<int:id>/', views.shows_detail, name='shows_detail'),

    # ================= EPISODES =================
    path('episode/<int:id>/', views.episode_detail, name='episode_detail'),
    path('watch-episode/<int:id>/', views.watch_episode, name='watch_episode'),
    path('watchlist-show/<int:show_id>/', views.toggle_tvshow_watchlist, name='toggle_tvshow_watchlist'),

    # ================= WATCHLIST =================
    path('my-watchlist/', views.watchlist_view, name='watchlist'),

    # ================= LIVE SEARCH =================
    path('live-search/', views.live_search, name='live_search'),

    # ================= CUSTOM ADMIN PANEL =================
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/movies/', views.admin_movies, name='admin_movies'),
    path('admin-panel/add-movie/', views.add_movie, name='add_movie'),

    path('admin-panel/shows/', views.admin_shows, name='admin_shows'),
    path('admin-panel/add-show/', views.add_show, name='add_show'),

    path('admin-panel/add-episode/', views.add_episode, name='add_episode'),
]