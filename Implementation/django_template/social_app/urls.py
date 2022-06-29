from django.urls import path

from . import views
# @Kerstin imports
from . import pause, weather
from . import friends
# TODO: @team add your source files here

urlpatterns = [
    #
    # ---------------------------------------------{Template Stuff}----------------------------------------------------#
    #  [source: views.py]
    path('signup/', views.signup),
    path('login/', views.signin),
    path('logout/', views.signout),
    path('check_auth/', views.check_auth),
    path('get_scores/', views.get_scores),
    path('edit_score/', views.edit_score),
    path('get_match/', views.get_match),
    path('host_match/', views.host_match),
    path('join_match/', views.join_match),
    path('end_match/', views.end_match),

    #
    # --------------------------------------------{Friendship Stuff}---------------------------------------------------#
    #  @Maxi urls for friendship [source: friends.py]
    path('get_friends/', friends.get_friends),
    path('get_names/', friends.get_names),
    path('add_friend/', friends.add_friend),
    path('get_followers/', friends.get_followers),
    path('disable_friend_info/', friends.disable_friend_info),
    path('get_friend_info_bool/', friends.get_friend_info_bool),


    #
    # --------------------------------------------{Pause Menu Stuff}---------------------------------------------------#
    #  @Kerstin urls for pause menu [source: pause.py]
    path('pause_game/', pause.pause_game),
    path('get_paused/', pause.get_paused),
    path('resume_game/', pause.resume_game),
    path('request_reset/', pause.request_reset),
    path('reset_level/', pause.reset_level),
    path('clear_reset/', pause.clear_reset),
    path('request_exit/', pause.request_exit),
    path('exit_level/', pause.exit_level),
    path('pause_menu_show_friends/', pause.pause_menu_show_friends),
    # ...

    #
    # ----------------------------------------------{Weather Stuff}----------------------------------------------------#
    #  @Kerstin urls for weather stuff [source: weather.py]

    # TODO: @team add your paths here
]
