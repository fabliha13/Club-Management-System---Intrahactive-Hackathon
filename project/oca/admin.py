from django.contrib import admin

from .models import club_panel,Event, Room, RoomBooking, BudgetRequest, Communication, EventReport

admin.site.register(Event)
admin.site.register(Room)
admin.site.register(RoomBooking)
admin.site.register(BudgetRequest)
admin.site.register(Communication)
admin.site.register(EventReport)

admin.site.register(club_panel)
