from django.contrib import admin

from .models import Player, Friendship, Match, WeatherTokens, WaitingList

# All this does is add these tables to the admin site, where you can view
# and add entries table entries for testing purposes.
# (e.g. http://<your-name>.pythonanywhere.com/admin)
# If you add any new tables, it doesn't hurt to register them here.
admin.site.register(Player)
admin.site.register(Friendship)
admin.site.register(Match)
admin.site.register(WeatherTokens)
admin.site.register(WaitingList)