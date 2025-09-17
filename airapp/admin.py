from django.contrib import admin
from .models import Flight, Book, Message

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('bus_name', 'source', 'dest', 'date', 'time', 'nos', 'rem', 'price')
    search_fields = ('bus_name', 'source', 'dest')
    list_filter = ('source', 'dest', 'date')

@admin.register(Book)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'get_flight_name', 'date', 'nos', 'status')
    list_filter = ('status', 'date')
    search_fields = ('name', 'email')

    def get_flight_name(self, obj):
        return obj.flight.bus_name
    get_flight_name.short_description = 'Flight Name'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'sent_on')
    search_fields = ('name', 'email')
    readonly_fields = ('sent_on',)
