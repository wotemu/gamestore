from django.contrib import admin
from .models import Developer, Player, Game, State, Transaction

# Register your models here.
admin.site.register(Developer)
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(State)
admin.site.register(Transaction)
