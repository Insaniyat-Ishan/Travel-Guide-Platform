from django.contrib import admin
from . models import traveler, Hotel, Room, BookRoom, Agency, Vehicle,BookVehicle
from .models import Airline, Plane,Seat, SeatBooking,Destination,UserFavorites,FavoriteLocation,VisitedPlace,FAQ,FavoriteHotel,Offer

# Register your models here.
admin.site.register(traveler)
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(BookRoom)
admin.site.register(Agency)
admin.site.register(Vehicle)
admin.site.register(BookVehicle)
admin.site.register(Destination)
admin.site.register(UserFavorites)
admin.site.register(FavoriteLocation)
admin.site.register(VisitedPlace)
admin.site.register(FAQ)
admin.site.register(FavoriteHotel)
admin.site.register(Offer)
#Ishan's code


@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')

@admin.register(Plane)
class PlaneAdmin(admin.ModelAdmin):
    list_display = ('name', 'airline', 'model', 'capacity')



admin.site.register(Seat)
admin.site.register(SeatBooking)
from django.contrib import admin
from .models import Review

# Register your models here.
admin.site.register(Review)


from django.contrib import admin
from .models import BookingFeedback

admin.site.register(BookingFeedback)
