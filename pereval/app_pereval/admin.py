from django.contrib import admin

from .models import AppUser, Coords, Level, Pereval, Images


class PerAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'add_time', 'level')

    # list_filter = ('user__username', 'add_time', 'level')


class CoordsAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude', 'height',)


class LevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'winter', 'summer', 'autumn', 'spring',)


admin.site.register(AppUser)
admin.site.register(Coords)
admin.site.register(Level)
admin.site.register(Pereval)
admin.site.register(Images)
