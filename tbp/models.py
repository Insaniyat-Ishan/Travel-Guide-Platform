from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms



# Create your models here.

class traveler(AbstractUser):
    username = models.CharField(max_length=150, primary_key=True)
    email = models.EmailField(unique=True)
    phone = models.IntegerField(null=True)
    age = models.PositiveIntegerField(null=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)



    def __str__(self):
        return self.username
    
class Hotel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='hotel_images/', null=True, blank=True)  # Provide a default image

    def __str__(self):
        return self.name


class Room(models.Model):
    TYPE_CHOICES = [
        ('Standard', 'Standard'),
        ('Deluxe', 'Deluxe'),
        ('Suite', 'Suite'),
    ]

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    room_number = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Standard')

    class Meta:
        unique_together = ('hotel', 'room_number')  # Partial key constraint

    def __str__(self):
        return f"{self.get_type_display()} Room {self.room_number} at {self.hotel.name}"



class Agency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='agency_images/', null=True, blank=True)  # Provide a default image

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    CAR_TYPE_CHOICES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Truck', 'Truck'),
        ('Van', 'Van'),
        ('Hatchback', 'Hatchback'),
        ('Convertible', 'Convertible'),
        ('Coupe', 'Coupe'),
    ]
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    car_type = models.CharField(max_length=100, choices=CAR_TYPE_CHOICES)
    license_no = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.car_type} ({self.license_no}) - {self.agency.name}"
    

class BookVehicle(models.Model):
    traveler = models.ForeignKey('Traveler', on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    booking_date = models.DateField()
    checkout_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.traveler.username}'s Booking from {self.booking_date} to {self.checkout_date}"

    def save(self, *args, **kwargs):
        if self.vehicle and self.booking_date and self.checkout_date and self.total_amount:
            price_per_day = self.vehicle.price
            booking_days = (self.checkout_date - self.booking_date).days
            total_price = price_per_day * booking_days
            self.due_amount = total_price - self.total_amount
        super().save(*args, **kwargs)
        
class BookRoom(models.Model):
    traveler = models.ForeignKey('Traveler', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    booking_date = models.DateField()
    checkout_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.traveler.username}'s Room Booking from {self.booking_date} to {self.checkout_date}"

    def save(self, *args, **kwargs):
        if self.room and self.booking_date and self.checkout_date and self.total_amount:
            price_per_day = self.room.price  # Assuming there's a price field in the Room model
            booking_days = (self.checkout_date - self.booking_date).days
            total_price = price_per_day * booking_days
            self.due_amount = total_price - self.total_amount
        super().save(*args, **kwargs)


#Ishan's code

class Airline(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Plane(models.Model):
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    capacity = models.IntegerField()
    arrival_country = models.CharField(max_length=100, default = "Bangladesh")  
    departure_country = models.CharField(max_length=100, default = "India")  

    def __str__(self):
        return f"{self.airline.name} - {self.name}"
    

User = get_user_model()


class Seat(models.Model):
    # Define choices for seat types
    ECONOMY = 'Economy'
    BUSINESS = 'Business'
    FIRST_CLASS = 'First Class'
    SEAT_TYPE_CHOICES = [
        (ECONOMY, 'Economy'),
        (BUSINESS, 'Business'),
        (FIRST_CLASS, 'First Class'),
    ]
    
    # Define model fields
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    seat_type = models.CharField(max_length=20, choices=SEAT_TYPE_CHOICES, default='Economy')

    def __str__(self):
        return f"{self.plane.name} - Seat {self.seat_number}"
class SeatBooking(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    def clean(self):
        # Check if there's already a booking for the same seat on the same date
        existing_bookings = SeatBooking.objects.filter(seat=self.seat, date=self.date)
        if self.pk:
            existing_bookings = existing_bookings.exclude(pk=self.pk)
        if existing_bookings.exists():
            raise ValidationError('Another booking exists for this seat on the same date.')

    def __str__(self):
        return f"{self.user.username} - {self.seat} - {self.date}"
    

class Destination(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='destination_images/')
    # Add any other fields you need for destinations

    def __str__(self):
        return self.name
    
    
class UserFavorites(models.Model):
    user = models.OneToOneField(traveler, on_delete=models.CASCADE)
    favorite_destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)
    favorite_vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    favorite_hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    favorite_airline = models.ForeignKey(Airline, on_delete=models.SET_NULL, null=True, blank=True)
    
from django.db import models
from django.contrib.auth import get_user_model
from .models import Destination

class FavoriteLocation(models.Model):
    traveler = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

    class Meta:
        # Ensure each user can select each favorite place only once
        unique_together = ('traveler', 'destination')
    
class VisitedPlace(models.Model):
    traveler = models.ForeignKey(traveler, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.traveler.username}'s visit to {self.location}"
    
from django.db import models
from django.contrib.auth import get_user_model

class FAQ(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
    
from django.contrib.auth import get_user_model

class FavoriteHotel(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    class Meta:
        # Ensure each user can select each favorite place only once
        unique_together = ('user', 'hotel')





class BookingFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username} at {self.created_at}"
from django.db import models
from django.contrib.auth import get_user_model
from .models import Hotel

User = get_user_model()

from django.db import models
from django.contrib.auth import get_user_model


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, null=True, blank=True)
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, null=True, blank=True)
    plane = models.ForeignKey('Plane', on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.hotel:
            return f"Review by {self.user.username} for {self.hotel.name}"
        elif self.plane:
            return f"Review by {self.user.username} for {self.plane.name}"
        elif self.agency:
            return f"Review by {self.user.username} for {self.agency.name}"
        else:
            return "Review"
        

from django.db import models
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.dispatch import receiver

class Offer(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.IntegerField(default=100)

    def __str__(self):
        return self.title

@receiver(post_save, sender=Offer)
def send_offer_notification(sender, instance, **kwargs):
    """
    A signal receiver which sends an email notification to all users
    when a new Offer is saved.
    """
    if kwargs['created']:  # Only send email if the Offer is newly created
        users = traveler.objects.all()
        subject = 'New Offer Available!'
        message = f"Check out our new offer: {instance.title}. Description: {instance.description}"
        from_email = 'matbarwalid@gmail.com'  # Change this to your email address
        recipient_list = [user.email for user in users]
        send_mail(subject, message, from_email, recipient_list)
