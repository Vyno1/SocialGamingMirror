from django.urls import path

from . import views, pause, friends, weather, gamestate, levelloader

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
    path('get_names/', friends.get_names),
    path('get_friends/', friends.get_friends),
    path('get_followers/', friends.get_followers),
    path('add_friend/', friends.add_friend),
    path('disable_friend_info/', friends.disable_friend_info),
    path('get_friend_info_bool/', friends.get_friend_info_bool),
    path('update_friendship_level/', friends.update_friendship_level),
    # ...

    #
    # --------------------------------------------{Pause Menu Stuff}---------------------------------------------------#
    #  @Kerstin urls for pause menu [source: pause.py]
    path('pause_game/', pause.pause_game),
    path('get_paused/', pause.get_paused),
    path('resume_game/', pause.resume_game),
    path('request_reset/', pause.request_reset),
    path('request_exit/', pause.request_exit),
    # ...

    #
    # ----------------------------------------------{Weather Stuff}----------------------------------------------------#
    #  @Kerstin urls for weather stuff [source: weather.py]

    # TODO: @team add your paths here

    #
    # --------------------------------------------{Game State Stuff}---------------------------------------------------#
    #  @Kerstin urls for pause menu [source: gamestate.py]

    # --------------------------------------------{Level Change Stuff}-------------------------------------------------#
    #  @Vyno urls for Level change [source: levelloader.py]
    path('update_level/', levelloader.update_level),
    path('get_update/', levelloader.get_update)
]
