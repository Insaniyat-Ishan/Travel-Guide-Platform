
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
import stripe
from .forms import BookingFeedbackForm, ProfileUpdateForm, TravelerLoginForm, TravelerRegistrationForm
from .forms import BookRoomForm,BookVehicleForm
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import TravelerUpdateForm
from .models import BookingFeedback, Destination, Hotel,Room,Vehicle,Agency
from .forms import AdvancedSearchForm,AdvancedCarSearchForm,BookRoom,BookVehicle
from django.utils import timezone
from django.db.models import Prefetch
from .models import SeatBooking, Plane,Offer
from .forms import SearchForm
from .forms import BookingForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ProfilePictureForm
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import ProfileUpdateForm, ProfilePictureForm
from .models import traveler
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import TravelerLoginForm
from django.shortcuts import render, redirect
from .forms import ProfilePictureForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import TravelerRegistrationForm



# Create your views here.

def index_view(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = TravelerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('signup_confirmation') 
    else:
        form = TravelerRegistrationForm()
    return render(request, 'signup.html', {'form': form})


def signup_confirmation(request):
    return render(request, 'signup_confirmation.html')



def login_view(request):
    if request.method == 'POST':
        form = TravelerLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page after successful login
            else:
                # Authentication failed, add error message to form
                form.add_error(None, "Invalid username or password.")
    else:
        form = TravelerLoginForm()

    return render(request, 'login.html', {'form': form})






def logout_view(request):
    logout(request)
    return redirect('index') 



def update_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after successful update
    else:
        form = ProfilePictureForm(instance=request.user)
    return render(request, 'update_profile_picture.html', {'form': form})


def update_profile(request):
    if request.method == 'POST':
        form = TravelerUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_updated')  # Redirect to a success page
    else:
        form = TravelerUpdateForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

def profile_updated(request):
    return render(request, 'profile_updated.html')


@login_required  # Ensures that only logged-in users can access this view
def view_profile(request):
    # Retrieve the traveler instance associated with the logged-in user
    profile = request.user

    # Pass the profile information to the template
    return render(request, 'profile.html', {'profile': profile})

from django.conf import settings
import stripe
from .models import Destination
stripe.api_key = settings.STRIPE_SECRET_KEY



@login_required
def book_room(request):
    if request.method == 'POST':
        payment_option = request.POST.get('payment_option')
        form = BookRoomForm(request.POST)
        if form.is_valid():
            if payment_option == 'card':
                try:
                    # Process payment with Stripe
                    charge = stripe.Charge.create(
                        amount=form.cleaned_data['total_amount'] * 100,  # Total amount in cents
                        currency='usd',
                        description='Booking Room Charge',
                        source=request.POST['stripeToken'],  # Token generated by Stripe.js
                    )
                    if charge.status == 'succeeded':
                        save_room_booking(request, form)
                        return redirect('booking_confirmation')
                    else:
                        messages.error(request, "Payment failed. Please try again.")
                except stripe.error.StripeError as e:
                    messages.error(request, str(e))
            elif payment_option == 'gateway':
                save_room_booking(request, form)
                return redirect('booking_confirmation')
    else:
        form = BookRoomForm()
    return render(request, 'book_room.html', {'form': form, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})

def save_room_booking(request, form):
    book_room = form.save(commit=False)
    book_room.traveler = request.user
    book_room.save()
    # Additional processing if needed


@login_required
def book_vehicle(request):
    if request.method == 'POST':
        payment_option = request.POST.get('payment_option')
        form = BookVehicleForm(request.POST)
        if form.is_valid():
            if payment_option == 'card':
                # Process payment with Stripe
                try:
                    # Create a charge
                    charge = stripe.Charge.create(
                        amount=form.cleaned_data['total_amount'] * 100,  # Total amount in cents
                        currency='usd',
                        description='Booking Vehicle Charge',
                        source=request.POST['stripeToken'],  # Token generated by Stripe.js
                    )
                    if charge.status == 'succeeded':
                        save_booking(request, form)
                        return redirect('booking_confirmation')
                    else:
                        # Handle failed payment
                        messages.error(request, "Payment failed. Please try again.")
                except stripe.error.StripeError as e:
                    # Handle Stripe errors
                    messages.error(request, str(e))
            elif payment_option == 'gateway':
                save_booking(request, form)
                return redirect('booking_confirmation')
    else:
        form = BookVehicleForm()
    return render(request, 'book_vehicle.html', {'form': form, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})

def save_booking(request, form):
    book_vehicle = form.save(commit=False)
    book_vehicle.traveler = request.user
    book_vehicle.save()

def booking_confirmation_view(request):
    return render(request, 'booking_confirmation.html')


# def hotels_list(request):
#     hotels = Hotel.objects.prefetch_related('room_set').all()  # Retrieve hotels with related rooms
#     return render(request, 'hotels_list.html', {'hotels': hotels})

# def agencies_list(request):
#     agencies = Agency.objects.prefetch_related('vehicle_set').all()
#     return render(request, 'agencies_list.html', {'agencies': agencies})


from django.shortcuts import render
from django.db.models import Avg
from .models import Hotel

def hotels_list(request):
    hotels = Hotel.objects.prefetch_related('room_set').annotate(avg_rating=Avg('review__rating'))
    return render(request, 'hotels_list.html', {'hotels': hotels})


from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from .models import Hotel

def hotel_details(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    avg_rating = hotel.review_set.aggregate(Avg('rating'))['rating__avg']
    if avg_rating is not None:
        avg_rating = round(avg_rating, 2)
    return render(request, 'hotel_details.html', {'hotel': hotel, 'avg_rating': avg_rating})




from django.shortcuts import render
from .models import Hotel, Review

def hotel_reviews(request, hotel_id):
    hotel = Hotel.objects.get(pk=hotel_id)
    reviews = Review.objects.filter(hotel=hotel)
    reviews_with_usernames = [(review, review.user.username) for review in reviews]
    return render(request, 'hotel_reviews.html', {'hotel': hotel, 'reviews_with_usernames': reviews_with_usernames})




# def agencies_list(request):
#     agencies = Agency.objects.prefetch_related('vehicle_set').all()
#     return render(request, 'agencies_list.html', {'agencies': agencies})

# from django.shortcuts import render
# from django.db.models import Avg
# from .models import Agency

# def agencies_list(request):
#     agencies = Agency.objects.prefetch_related('vehicle_set').annotate(avg_rating=Avg('review__rating'))
#     for agency in agencies:
#         if agency.avg_rating is not None:
#             agency.avg_rating = round(agency.avg_rating, 2)  # Round average rating to 2 decimal points
#     return render(request, 'agencies_list.html', {'agencies': agencies})

from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from .models import Agency

def agencies_list(request):
    agencies = Agency.objects.prefetch_related('vehicle_set').annotate(avg_rating=Avg('review__rating'))
    # for agency in agencies:
    #     if agency.avg_rating is not None:
    #         agency.avg_rating = round(agency.avg_rating, 2)  # Round average rating to 2 decimal points
    return render(request, 'agencies_list.html', {'agencies': agencies})


def agency_details(request, agency_id):
    agency = get_object_or_404(Agency, pk=agency_id)
    avg_rating = agency.review_set.aggregate(Avg('rating'))['rating__avg']
    if avg_rating is not None:
        avg_rating = round(avg_rating, 2)
    return render(request, 'agency_details.html', {'agency': agency, 'avg_rating': avg_rating})






from django.shortcuts import render
from .models import Agency, Review

def agency_reviews(request, agency_id):
    agency = Agency.objects.get(pk=agency_id)
    reviews = Review.objects.filter(agency=agency)
    return render(request, 'agency_reviews.html', {'agency': agency, 'reviews': reviews})






def advanced_search(request):
    form = AdvancedSearchForm(request.GET)
    hotels = []
    if form.is_valid():
        hotels = form.filter_hotels()
    return render(request, 'advanced_search.html', {'form': form, 'hotels': hotels})

def advanced_car_search(request):
    form = AdvancedCarSearchForm(request.GET)
    agencies = []
    if form.is_valid():
        agencies = form.filter_agencies()
    return render(request, 'advanced_car_search.html', {'form': form, 'agencies': agencies})

def booked_rooms(request):
    today = timezone.now().date()
    past_booked_rooms = BookRoom.objects.filter(traveler=request.user, checkout_date__lt=today).select_related('room__hotel')
    upcoming_booked_rooms = BookRoom.objects.filter(traveler=request.user, booking_date__gte=today).select_related('room__hotel')
    current_booked_rooms = BookRoom.objects.filter(
        traveler=request.user,
        booking_date__lte=today,
        checkout_date__gte=today
    ).select_related('room__hotel')

    return render(request, 'booked_rooms.html', {
        'past_booked_rooms': past_booked_rooms,
        'upcoming_booked_rooms': upcoming_booked_rooms,
        'current_booked_rooms': current_booked_rooms
    })
    
def booked_vehicles(request):
    today = timezone.now().date()
    past_booked_vehicles = BookVehicle.objects.filter(traveler=request.user, checkout_date__lt=today).select_related('vehicle__agency')
    upcoming_booked_vehicles = BookVehicle.objects.filter(traveler=request.user, booking_date__gte=today).select_related('vehicle__agency')
    current_booked_vehicles = BookVehicle.objects.filter(
        traveler=request.user,
        booking_date__lte=today,
        checkout_date__gte=today
    ).select_related('vehicle__agency')

    return render(request, 'booked_vehicles.html', {
        'past_booked_vehicles': past_booked_vehicles,
        'upcoming_booked_vehicles': upcoming_booked_vehicles,
        'current_booked_vehicles': current_booked_vehicles
    })    
    
#Ishan's code

def book_flight(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Process the form data and save the booking
            airline = form.cleaned_data['airlines']
            plane = form.cleaned_data['planes']
            seat = form.cleaned_data['seats']
            departure_country = form.cleaned_data['departure_country']
            arrival_country = form.cleaned_data['arrival_country']
            date = form.cleaned_data['date']

            # Retrieve seat type and price
            seat_type = seat.seat_type
            price = seat.price

            try:
                booking = SeatBooking.objects.create(
                    seat=seat,
                    user=request.user,  # Assuming the user is authenticated
                    date=date,
                )
            except ValidationError as e:
                messages.error(request, e.message)
                return redirect('book_flight')

            # Redirect to a confirmation page or any other page
            messages.success(request, 'Booking successful!')
            return redirect('booking_confirmation')  # Adjust the URL name as needed
        else:
            # If form is not valid, re-render the form with error messages
            messages.error(request, 'This seat is already booked for the selected date.')
    else:
        form = BookingForm()

    return render(request, 'book_flight.html', {'form': form})

def booking_confirmation(request):
    return render(request, 'booking_confirmation.html')

def search_vacant_seats(request):
    form = SearchForm(request.GET)

    if form.is_valid():
        airline = form.cleaned_data.get('airline')
        plane = form.cleaned_data.get('plane')
        date = form.cleaned_data.get('date')

        if plane is not None:
            # Get all seats from the specified plane
            all_seats = plane.seat_set.all()

            # Filter seats that are not booked on the specified date
            booked_seats = SeatBooking.objects.filter(date=date, seat__in=all_seats).values_list('seat', flat=True)
            vacant_seats = all_seats.exclude(id__in=booked_seats)

            return render(request, 'vacant_seats.html', {'form': form, 'vacant_seats': vacant_seats})

    return render(request, 'search_vacant_seats.html', {'form': form})

def view_flight_details(request, flight_id):
    # Retrieve the specific flight using the flight_id
    flight = get_object_or_404(Plane, pk=flight_id)

    # You can customize this rendering based on your model structure
    return render(request, 'flight_details.html', {'flight': flight})

def home(request):
    available_flights = Plane.objects.all()  # Update this query as needed
    return render(request, 'home.html', {'available_flights': available_flights})

def view_all_flight_details(request):
    all_flights = Plane.objects.all()  # Retrieve all flights from the database
    return render(request, 'all_flight_details.html', {'all_flights': all_flights})


from django.shortcuts import render
from .models import SeatBooking

def view_booked_flights(request):
    # Fetch booked flights for the current user
    booked_flights = SeatBooking.objects.filter(user=request.user).select_related('seat__plane')

    return render(request, 'booked_flights.html', {'booked_flights': booked_flights})

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import ProfileUpdateForm, ProfilePictureForm
from .models import traveler

def update_profile(request):
    User = get_user_model()
    profile = traveler.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        picture_form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid() and picture_form.is_valid():
            # Check if the "Remove Profile Picture" checkbox is checked
            if 'remove_profile_picture' in request.POST:
                profile.profile_picture.delete()  # Delete the profile picture file
                profile.profile_picture = None  # Set profile picture field to None
            form.save()
            picture_form.save()
            return redirect('view_profile')
    else:
        form = ProfileUpdateForm(instance=profile)
        picture_form = ProfilePictureForm(instance=profile)
    return render(request, 'update_profile.html', {'form': form, 'picture_form': picture_form})

def remove_profile_picture(request):
    User = get_user_model()
    profile = traveler.objects.get(username=request.user.username)
    if profile.profile_picture:
        profile.profile_picture.delete()  # Delete the profile picture file
        profile.profile_picture = None  # Set profile picture field to None
        profile.save()  # Save the profile instance
    return redirect('view_profile')


def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, 'destination_list.html', {'destinations': destinations})

def destination_detail(request, destination_id):
    destination = get_object_or_404(Destination, pk=destination_id)
    return render(request, 'destination_detail.html', {'destination': destination})

from django.shortcuts import render, redirect
from .models import UserFavorites
from .forms import UserFavoritesForm

def set_user_favorites(request):
    # Get the current user
    user = request.user

    # Attempt to get an existing UserFavorites instance for the user
    try:
        user_favorites = UserFavorites.objects.get(user=user)
    except UserFavorites.DoesNotExist:
        user_favorites = None

    if request.method == 'POST':
        # Create a form instance with the POST data
        form = UserFavoritesForm(request.POST, instance=user_favorites)
        
        # Check if the form is valid
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Redirect to a success page or any other page
            return redirect('home')  # Change 'home' to the name of your desired destination page
    else:
        # If it's a GET request, create a form instance with existing user favorites (if available)
        form = UserFavoritesForm(instance=user_favorites)
    
    # Render the template with the form
    return render(request, 'set_user_favorites.html', {'form': form})


from django.shortcuts import render
from .models import UserFavorites

def show_user_favorites(request):
    # Get the current user
    user = request.user

    # Attempt to get an existing UserFavorites instance for the user
    try:
        user_favorites = UserFavorites.objects.get(user=user)
    except UserFavorites.DoesNotExist:
        user_favorites = None

    return render(request, 'show_user_favorites.html', {'user_favorites': user_favorites})

from django.shortcuts import render, redirect
from .models import VisitedPlace
from .forms import VisitedPlaceForm

def add_visited_place(request):
    if request.method == 'POST':
        form = VisitedPlaceForm(request.POST)
        if form.is_valid():
            visited_place = form.save(commit=False)
            visited_place.traveler = request.user  # Assuming user is authenticated
            visited_place.save()
            return redirect('home')  # Redirect to a page showing all visited places
    else:
        form = VisitedPlaceForm()
    return render(request, 'add_visited_place.html', {'form': form})

from django.shortcuts import render
from .models import VisitedPlace

def all_visited_places(request):
    visited_places = VisitedPlace.objects.all()
    return render(request, 'all_visited_places.html', {'visited_places': visited_places})

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import FAQ
from .forms import FAQForm

def faq(request):
    faqs = FAQ.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            faq_instance = form.save(commit=False)
            faq_instance.user = request.user
            faq_instance.save()
            return redirect('faq')
    else:
        form = FAQForm()
    return render(request, 'faq.html', {'faqs': faqs, 'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FavoriteHotel
from .forms import FavoriteHotelForm

@login_required
def favorite_hotels(request):
    favorite_hotels = FavoriteHotel.objects.filter(user=request.user)
    return render(request, 'favorite_hotels.html', {'favorite_hotels': favorite_hotels})

@login_required
def add_favorite_hotel(request):
    if request.method == 'POST':
        form = FavoriteHotelForm(request.POST)
        if form.is_valid():
            hotel = form.cleaned_data['hotel']
            # Check if the favorite hotel already exists for the current user
            if not FavoriteHotel.objects.filter(user=request.user, hotel=hotel).exists():
                favorite_hotel = FavoriteHotel(user=request.user, hotel=hotel)
                favorite_hotel.save()
                return redirect('favorite_hotels')
            else:
                # Handle case where the favorite hotel already exists for the user
                return render(request, 'add_favorite_hotel.html', {'form': form, 'error_message': 'You have already added this hotel to your favorites.'})
    else:
        form = FavoriteHotelForm()
    return render(request, 'add_favorite_hotel.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FavoriteLocation
from .forms import FavoriteLocationForm

@login_required
def favorite_locations(request):
    favorite_locations = FavoriteLocation.objects.filter(traveler=request.user)
    return render(request, 'favorite_locations.html', {'favorite_locations': favorite_locations})

@login_required
def add_favorite_location(request):
    if request.method == 'POST':
        form = FavoriteLocationForm(request.POST)
        if form.is_valid():
            destination = form.cleaned_data['destination']
            # Check if the favorite location already exists for the current user
            if not FavoriteLocation.objects.filter(traveler=request.user, destination=destination).exists():
                favorite_location = form.save(commit=False)
                favorite_location.traveler = request.user
                favorite_location.save()
                return redirect('favorite_locations')
            else:
                # Handle case where the favorite location already exists for the user
                error_message = 'You have already added this location to your favorites.'
                return render(request, 'add_favorite_location.html', {'form': form, 'error_message': error_message})
    else:
        form = FavoriteLocationForm()
    return render(request, 'add_favorite_location.html', {'form': form})

@login_required
def user_vehicle_due_amount(request):
    current_user = request.user
    
    # Fetch all BookVehicle instances associated with the current user
    bookings = BookVehicle.objects.filter(traveler=current_user)
    
    context = {
        'bookings': bookings
    }
    return render(request, 'user_vehicle_due_amount.html', context)

@login_required
def user_hotel_due_amount(request):
    current_user = request.user
    
    # Fetch all BookHotel instances associated with the current user
    bookings = BookRoom.objects.filter(traveler=current_user)
    
    context = {
        'bookings': bookings
    }
    return render(request, 'user_hotel_due_amount.html', context)


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required








# views.py
def provide_feedback(request):
    if request.method == 'POST':
        form = BookingFeedbackForm(request.POST)
        if form.is_valid():
            feedback_text = form.cleaned_data['feedback']
            # Assuming you have a logged-in user
            user = request.user
            # Save feedback to the database
            BookingFeedback.objects.create(user=user, feedback=feedback_text)
            # Redirect to a thank you page or any other appropriate page
            return redirect('home')
    else:
        form = BookingFeedbackForm()
    return render(request, 'provide_feedback.html', {'form': form})





from django.shortcuts import render
from django.http import JsonResponse
from .models import Review, Hotel, Plane
from django.http import JsonResponse
from .models import Hotel, Plane, Review, Agency
from django.shortcuts import render

def review_and_rate(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        name = request.POST.get('name')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if type == 'hotel':
            hotel = Hotel.objects.get(name=name)
            Review.objects.create(
                user=request.user,
                hotel=hotel,
                rating=rating,
                comment=comment
            )
        elif type == 'flight':
            plane = Plane.objects.get(name=name)
            Review.objects.create(
                user=request.user,
                plane=plane,
                rating=rating,
                comment=comment
            )
        elif type == 'agency':
            agency = Agency.objects.get(name=name)
            Review.objects.create(
                user=request.user,
                agency=agency,
                rating=rating,
                comment=comment
            )
            
        return JsonResponse({'success': True})
    else:
        hotels = Hotel.objects.all()
        planes = Plane.objects.all()
        agencies = Agency.objects.all()
        return render(request, 'review_and_rate.html', {'hotels': hotels, 'planes': planes, 'agencies': agencies})

from django.http import JsonResponse
from .models import Hotel, Plane, Agency

def get_names(request):
    type = request.GET.get('type')
    names = []

    if type == 'flight':
        # Fetch flight names from the Plane model
        planes = Plane.objects.all()
        names = [plane.name for plane in planes]
    elif type == 'hotel':
        # Fetch hotel names from the Hotel model
        hotels = Hotel.objects.all()
        names = [hotel.name for hotel in hotels]
    elif type == 'agency':
        # Fetch agency names from the Agency model
        agencies = Agency.objects.all()
        names = [agency.name for agency in agencies]

    return JsonResponse({'names': names})



def submit_feedback(request):
    # Add your code to handle the submission of feedback
    # This could involve saving the feedback to the database or performing other actions
    return redirect('home')  # Redirect to the home page or any other appropriate page

from django.shortcuts import render
from .models import Offer

def offers_view(request):
    offers = Offer.objects.all()
    return render(request, 'offers.html', {'offers': offers})

from django.shortcuts import render, get_object_or_404
from .models import Offer

def offer_detail(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    return render(request, 'offer_detail.html', {'offer': offer})
