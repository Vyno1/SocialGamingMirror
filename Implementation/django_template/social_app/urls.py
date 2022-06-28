from django.urls import path

from . import views
# @Kerstin imports
from . import pause, weather
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
    path('get_friends/', views.get_friends),
    path('get_names/', views.get_names),
    path('add_friend/', views.add_friend),
    path('get_match/', views.get_match),
    path('host_match/', views.host_match),
    path('join_match/', views.join_match),
    # @Kerstin removed pass_ball/
    path('end_match/', views.end_match),
    # @Maxi added:
    path('get_followers/', views.get_followers),
    path('disable_friend_info/', views.disable_friend_info),
    path('get_friend_info_bool/', views.get_friend_info_bool),

    # TODO: @team add your paths here
    # syntax: path(url, method)

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

    #
    # ----------------------------------------------{Weather Stuff}----------------------------------------------------#
    #  @Kerstin urls for weather stuff [source: weather.py]
]
