from django.contrib import admin

# Register your models here.
from .models import Golfer, Pick, Punter, Event
from .forms import PickForm

admin.site.register(Event)
admin.site.register(Golfer)
#admin.site.register(Pick)
admin.site.register(Punter)

@admin.register(Pick)
class PickAdmin(admin.ModelAdmin):
    list_filter = ('event',)
    form = PickForm
