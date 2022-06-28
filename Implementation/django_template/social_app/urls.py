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

    # TODO: @team add your paths here
    # syntax: path(url, method)


]
