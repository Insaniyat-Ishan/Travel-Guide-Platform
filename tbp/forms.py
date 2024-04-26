from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import traveler
from .models import BookRoom,Room,Hotel,BookVehicle,Agency,Vehicle
from django.core.exceptions import ValidationError
User = get_user_model()
#Ishan's code
from .models import Airline, Plane, Seat, SeatBooking
from datetime import date

class TravelerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.IntegerField(required=False)
    age = forms.IntegerField(required=False)
    name = forms.CharField(required=True)
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'age', 'name', 'gender', 'password1', 'password2')


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:  # Example validation: Minimum password length of 8 characters
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.age = self.cleaned_data['age']
        user.name = self.cleaned_data['name']
        user.gender = self.cleaned_data['gender']
        if commit:
            user.save()
        return user
    
class TravelerLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class TravelerUpdateForm(forms.ModelForm):
    class Meta:
        model = traveler
        fields = ['email', 'phone', 'age', 'name', 'gender']

class ProfileUpdateForm(forms.ModelForm):
    remove_profile_picture = forms.BooleanField(label='Remove Profile Picture', required=False)

    class Meta:
        model = traveler
        fields = ['username', 'email', 'phone', 'age', 'name', 'gender']

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = traveler
        fields = ['profile_picture']

class BookRoomForm(forms.ModelForm):
    total_amount = forms.DecimalField(max_digits=10, decimal_places=2, label='Total Amount')
    booking_date = forms.DateField(label='Booking_date', widget=forms.DateInput(attrs={'type': 'date'}))
    checkout_date = forms.DateField(label='Checkout_date', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = BookRoom
        fields = ['room', 'booking_date', 'checkout_date', 'total_amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            # Calculate and set the due amount
            if self.instance.room and self.instance.booking_date and self.instance.checkout_date:
                price_per_day = self.instance.room.price
                booking_days = (self.instance.checkout_date - self.instance.booking_date).days
                total_price = price_per_day * booking_days
                self.instance.due_amount = total_price - self.instance.total_amount

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        booking_date = cleaned_data.get('booking_date')
        checkout_date = cleaned_data.get('checkout_date')
        total_amount = cleaned_data.get('total_amount')

        # Add validation for total_amount
        if total_amount is None:
            raise forms.ValidationError('Total amount is required.')

        # Add any additional validation logic for total_amount here

        if room and booking_date and checkout_date:
            existing_bookings = BookRoom.objects.filter(room=room)
            for booking in existing_bookings:
                if (booking.booking_date <= checkout_date) and (booking.checkout_date >= booking_date):
                    raise forms.ValidationError('Another booking exists within this duration')

        return cleaned_data
    
class BookVehicleForm(forms.ModelForm):

    total_amount = forms.DecimalField(label='Total Amount')
    booking_date = forms.DateField(label='Booking_date', widget=forms.DateInput(attrs={'type': 'date'}))
    checkout_date = forms.DateField(label='Checkout_date', widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = BookVehicle
        fields = ['vehicle', 'booking_date', 'checkout_date', 'total_amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            # Calculate and set the due amount
            if self.instance.vehicle and self.instance.booking_date and self.instance.checkout_date:
                price_per_day = self.instance.vehicle.price
                booking_days = (self.instance.checkout_date - self.instance.booking_date).days
                total_price = price_per_day * booking_days
                self.instance.due_amount = total_price - self.instance.total_amount

    def clean(self):
        cleaned_data = super().clean()
        vehicle = cleaned_data.get('vehicle')
        booking_date = cleaned_data.get('booking_date')
        checkout_date = cleaned_data.get('checkout_date')
        total_amount = cleaned_data.get('total_amount')

        if vehicle and booking_date and checkout_date:
            existing_bookings = BookVehicle.objects.filter(vehicle=vehicle)
            for booking in existing_bookings:
                if (booking.booking_date <= checkout_date) and (booking.checkout_date >= booking_date):
                    raise forms.ValidationError('Another booking exists within this duration')

        return cleaned_data
    
from django.db.models import Avg     
    
class AdvancedSearchForm(forms.Form):
    location = forms.CharField(required=False)
    min_price = forms.DecimalField(required=False, min_value=0)
    max_price = forms.DecimalField(required=False, min_value=0)
    room_type = forms.ChoiceField(choices=Room.TYPE_CHOICES, required=False)
    min_avg_rating = forms.IntegerField(required=False, min_value=1, max_value=5)  # Rename to min_avg_rating

    def filter_hotels(self):
        queryset = Hotel.objects.all()

        location = self.cleaned_data.get('location')
        min_price = self.cleaned_data.get('min_price')
        max_price = self.cleaned_data.get('max_price')
        room_type = self.cleaned_data.get('room_type')
        min_avg_rating = self.cleaned_data.get('min_avg_rating')  # Retrieve min_avg_rating value

        if location:
            queryset = queryset.filter(location__icontains=location)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if room_type:
            queryset = queryset.filter(room__type=room_type)    
        if min_avg_rating:
            queryset = queryset.annotate(avg_rating=Avg('review__rating')).filter(avg_rating__gte=min_avg_rating)  # Calculate average rating and apply filter

        return queryset.distinct()
    
    
from django.db.models import Avg
from .models import Review

class AdvancedCarSearchForm(forms.Form):
    location = forms.CharField(required=False)
    min_price = forms.DecimalField(required=False, min_value=0)
    max_price = forms.DecimalField(required=False, min_value=0)
    car_type = forms.ChoiceField(choices=Vehicle.CAR_TYPE_CHOICES, required=False)
    min_avg_rating = forms.IntegerField(required=False, min_value=1, max_value=5)

    def filter_agencies(self):
        queryset = Agency.objects.all()

        location = self.cleaned_data.get('location')
        min_price = self.cleaned_data.get('min_price')
        max_price = self.cleaned_data.get('max_price')
        car_type = self.cleaned_data.get('car_type')
        min_avg_rating = self.cleaned_data.get('min_avg_rating')

        if location:
            queryset = queryset.filter(location__icontains=location)
        if min_price:
            queryset = queryset.filter(vehicle__price__gte=min_price)
        if max_price:
            queryset = queryset.filter(vehicle__price__lte=max_price)
        if car_type:
            queryset = queryset.filter(vehicle__car_type=car_type)
        if min_avg_rating:
            # Filter by average rating of vehicles based on Review model associated with Agency
            queryset = queryset.annotate(avg_rating=Avg('review__rating')).filter(avg_rating__gte=min_avg_rating)

        return queryset.distinct()
    
    
#Ishan's code
class BookingForm(forms.Form):
    airlines = forms.ModelChoiceField(queryset=Airline.objects.all(), label='Select Airline')
    planes = forms.ModelChoiceField(queryset=Plane.objects.all(), label='Select Plane')
    seats = forms.ModelChoiceField(queryset=Seat.objects.all(), label='Select Seat')
    date = forms.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}))
    departure_country = forms.CharField(max_length=100, label='Departure Country', required=False)
    arrival_country = forms.CharField(max_length=100, label='Arrival Country', required=False)

    def clean(self):
        cleaned_data = super().clean()

        # Get the selected seat and date
        selected_seat = cleaned_data.get('seats')
        selected_date = cleaned_data.get('date')

        # Check if the seat is already booked on the selected date
        if SeatBooking.objects.filter(seat=selected_seat, date=selected_date).exists():
            raise forms.ValidationError('This seat is already booked on the selected date.')

        return cleaned_data
class SearchForm(forms.Form):
    airline = forms.ModelChoiceField(queryset=Airline.objects.all(), required=False)
    plane = forms.ModelChoiceField(queryset=Plane.objects.all(), required=False)
    date = forms.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}))



from django import forms
from .models import UserFavorites

class UserFavoritesForm(forms.ModelForm):
    class Meta:
        model = UserFavorites
        fields = ['favorite_destination', 'favorite_vehicle', 'favorite_hotel', 'favorite_airline']
        
# forms.py
from django import forms
from .models import VisitedPlace

class VisitedPlaceForm(forms.ModelForm):
    class Meta:
        model = VisitedPlace
        fields = ['location', 'description']
        
from django import forms
from .models import FAQ

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question']

from django import forms
from .models import FavoriteHotel

class FavoriteHotelForm(forms.ModelForm):
    class Meta:
        model = FavoriteHotel
        fields = ['hotel']
        
from django import forms
from .models import FavoriteLocation

class FavoriteLocationForm(forms.ModelForm):
    class Meta:
        model = FavoriteLocation
        fields = ['destination']


class BookingFeedbackForm(forms.Form):
    feedback = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

# forms.py
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    hotel_name = forms.CharField(max_length=255)  # Add a field for the hotel name

    class Meta:
        model = Review
        fields = ['hotel_name', 'rating', 'comment']
        
        
