from django.urls import path

from . import views, pause, friends, weather, gamestate, levelloader, invite, lobby, betweenlevels, steps, \
    gravity_manager, collectables, exit_and_time

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

    # --------------------------------------------{Exit / Time Stuff}------------------------------------------------- #

    # @Maxi
    path('handle_quit/', exit_and_time.handle_quit),
    path('set_quit/', exit_and_time.set_quit),
    path('get_localtime/', exit_and_time.get_localtime),
    path('send_localtime/', exit_and_time.send_localtime),

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
    # @Robin urls for invite and skinselect
    path('get_mutualfriends/', friends.get_mutualfriends),
    # ...

    #
    # --------------------------------------------{Pause Menu Stuff}---------------------------------------------------#
    #  @Kerstin urls for pause menu [source: pause.py]
    path('pause_game/', pause.pause_game),
    path('get_paused/', pause.get_paused),
    path('resume_game/', pause.resume_game),
    path('reset_game/', pause.reset_game),
    path('exit_game/', pause.exit_game),
    # ...

    #
    # ----------------------------------------------{Weather Stuff}----------------------------------------------------#
    #  @Kerstin urls for weather stuff [source: weather.py]
    path('create_weather_table/', weather.create_weather_table),
    path('store_current_weather/', weather.set_current_weather),
    path('load_tokens/', weather.get_weather_info),
    path('store_weather_info/', weather.update_player_weather),
    # TODO: @team add your paths here

    #
    # --------------------------------------------{Game State Stuff}---------------------------------------------------#
    #  @Kerstin urls for pause menu [source: gamestate.py]

    # --------------------------------------------{Level Change Stuff}-------------------------------------------------#
    #  @Vyno urls for Level change [source: levelloader.py]
    path('update_level/', levelloader.update_level),
    path('get_update/', levelloader.get_update),
    path('ask_for_change/', levelloader.ask_for_change),
    path('subtract_steps/', levelloader.subtract_steps),

    # --------------------------------------------{Between Level Stuff}------------------------------------------------#
    #  @Maxi urls for screen between the levels [source: betweenlevels.py]

    path('get_levels_unlocked/', betweenlevels.get_levels_unlocked),
    path('increase_levels_unlocked/', betweenlevels.increase_levels_unlocked),
    path('get_names/', betweenlevels.get_names),
    path('get_match_infos/', betweenlevels.get_match_infos),
    path('is_friendship_updated/', betweenlevels.is_friendship_updated),
    path('update_friendship/', betweenlevels.update_friendship),
    path('check_exit/', betweenlevels.check_exit),
    path('exit_level/', betweenlevels.exit_level),
    path('check_continue/', betweenlevels.check_continue),

    # ---------------------------------------------{Lobby Stuff}-------------------------------------------------------#
    # @Robin urls for lobby
    path('addHostLobby/', lobby.addHostLobby),
    path('findLobby/', lobby.findLobby),
    path('wait/', lobby.wait),
    path('setJoinedReady/', lobby.setJoinedReady),
    path('checkJoinedReady/', lobby.checkJoinedReady),
    path('startGame/', lobby.startGame),
    path('checkIfstarted/', lobby.checkIfStarted),
    path('leaveLobby/', lobby.leaveLobby),
    path('isHost/', lobby.isHost),
    path('checkIfAlone/', lobby.checkIfAlone),
    path('isFriend/', lobby.isFriend),

    path('setSkin/', lobby.setSkin),
    path('checkOtherSkin/', lobby.checkOtherSkin),

    # -------------------------------------------------{Urls for Invites}------------------------------
    # @Robin
    path('inviteFriend/', invite.inviteFriend),
    path('checkIfInvited/', invite.checkIfInvited),
    path('acceptInvite/', invite.acceptInvite),
    path('declineInvite/', invite.declineInvite),
    path('start/', invite.start),
    path('cancel/', invite.cancel),
    path('checkAnswer/', invite.checkAnswer),

    # -----------------------------------------------------{Utls for steps]-----------------------------
    # @Robin
    path('getSteps/', steps.getSteps),

    # --------------------------------------------{Gravity Object Stuff}-----------------------------------------------#
    # @Vyno
    path('setStartState/', gravity_manager.set_start_state),
    path('updateObjectState/', gravity_manager.update_object_state),
    path('askForUpdateBool/', gravity_manager.send_update_bool),
    path('askForUpdateObjectGravities/', gravity_manager.send_object_gravities),

    # --------------------------------------------{Collectable Stuff}--------------------------------------------------#
    # @Vyno
    path('checkIfColHost/', collectables.check_if_already_collected_host),
    path('checkIfColJoin/', collectables.check_if_already_collected_joined),
    path('updateCol/', collectables.update_collection)
]
