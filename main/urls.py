from django.conf.urls import url, include
from django.contrib import admin
from apps.gameapp.models import Game, GameType
from apps.loginreg.models import User as U

class UAdmin(admin.ModelAdmin):
    pass
admin.site.register(U, UAdmin)
class GameTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(GameType, GameTypeAdmin)
class GameAdmin(admin.ModelAdmin):
    pass
admin.site.register(Game, GameAdmin)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.gameapp.urls')),
    url(r'^', include('apps.loginreg.urls'))
]
