from django.urls import path, include

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path("loguser", views.login_user, name="loguser"),
    path('login', views.login_view, name='login'),
    path('developer', views.developer_view, name='developer'),
    path('logout', views.logout_view, name='logout'),
    path('signup', views.signup, name='signup'),
    path('catalog', views.catalog, name="catalog"),
    path('games/<int:game_id>/info', views.game_info, name="game_info"),
    path('games/<int:game_id>/play', views.play_game, name="play_game"),
    path('payment/success/', views.payment_success, name="payment_success"),
    path('payment/cancel', views.payment_cancel, name="payment_cancel"),
    path('payment/error', views.payment_error, name="payment_error"),
    path("developer/mygames", views.developer_games, name='developer_games'),
    path("developer/publish", views.publish_page_view, name='publish'),
    path("developer/publish_game", views.create_game, name='publish_game'),
    path('developer/games/<int:game_id>/edit', views.edit_game, name='editgame'),
    path('developer/games/<int:game_id>/update', views.edit_game_update, name='updategame'),
    path('developer/games/<int:game_id>/delete', views.edit_game_delete, name='deletegame'),
    path('service/score', views.submit_score, name="submit_score"),
    path('service/state', views.submit_state, name="submit_state"),
    path('service/load', views.load_game_state, name="load_game_state"),
    path("facebook", views.facebook_handler, name="facebook_handler"),
    path("home", views.home, name="home"),
    path("search", views.search, name="search"),

]
