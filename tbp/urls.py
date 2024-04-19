from django.urls import path,include
from . import views
from .views import agency_details, agency_reviews, booking_confirmation, hotel_details, hotel_reviews, provide_feedback, register, login_view, search_vacant_seats, submit_feedback, view_all_flight_details, view_booked_flights, view_flight_details
from .views import view_profile,booking_confirmation_view,offers_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('', views.index_view, name='index'),
    path('home/', views.home, name='home'),
    path('signup/', register, name='signup'),
    path('signup/confirmation/', views.signup_confirmation, name='signup_confirmation'),
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('reset_password/', views.reset_password, name='reset_password'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset.html'  # Updated path
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'  # Updated path
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html'  # Updated path
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'  # Updated path
         ),
         name='password_reset_complete'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('profile_updated/', views.profile_updated, name='profile_updated'),
    path('profile/', view_profile, name='view_profile'),
    path('book_room/', views.book_room, name='book_room'),
    path('booking-confirmation/', booking_confirmation_view, name='booking_confirmation'), 
    path('hotels/', views.hotels_list, name='hotels_list'),
    path('advanced-search/', views.advanced_search, name='advanced_search'),
    path('book_vehicle/', views.book_vehicle, name='book_vehicle'),
    path('advanced-car-search/', views.advanced_car_search, name='advanced_car_search'),
    path('Agencies/', views.agencies_list, name='agencies_list'),
    path('booked_rooms/', views.booked_rooms, name='booked_rooms'),
    path('booked_vehicles/', views.booked_vehicles, name='booked_vehicles'),
    path('book-flight/', views.book_flight, name='book_flight'),
    path('search-vacant-seats/', search_vacant_seats, name='search_vacant_seats'),
    path('flight/<int:flight_id>/', view_flight_details, name='view_flight_details'),
    path('view_all_flight_details/', view_all_flight_details, name='view_all_flight_details'),
    path('update_profile_picture/', views.update_profile_picture, name='update_profile_picture'),
    path('profile/<str:username>/', views.view_profile, name='profile'),
    path('profile_updated/', views.profile_updated, name='profile_updated'),
    path('booked-flights/', view_booked_flights, name='booked_flights'),
    path('destination_list/', views.destination_list, name='destination_list'),
    path('destination/<int:destination_id>/', views.destination_detail, name='destination_detail'),
    path('set_user_favorites/',views.set_user_favorites,name = 'set_user_favorites'),
    path('show_user_favorites/',views.show_user_favorites,name = 'show_user_favorites'),
    path('add_visited_place/',views.add_visited_place,name = 'add_visited_place'),
    path('all_visited_places/',views.all_visited_places,name = 'all_visited_places'),
    path('faq/',views.faq,name = 'faq'),
    path('favorite_hotels/',views.favorite_hotels,name = 'favorite_hotels'),
    path('add_favorite_hotel',views.add_favorite_hotel,name = 'add_favorite_hotel'),
    path('favorite_locations/',views.favorite_locations,name = 'favorite_locations'),
    path('add_favorite_location/',views.add_favorite_location,name = 'add_favorite_location'),
    path('user_vehicle_due_amount/',views.user_vehicle_due_amount,name = 'user_vehicle_due_amount'),
    path('user_hotel_due_amount/',views.user_hotel_due_amount,name = 'user_hotel_due_amount'),
    path('provide-feedback/', provide_feedback, name='provide_feedback'),
    path('submit-feedback/', submit_feedback, name='submit_feedback'),
    path('review_and_rate/', views.review_and_rate, name='review_and_rate'),
    path('get_names/', views.get_names, name='get_names'),
    path('hotel/<int:hotel_id>/reviews/', hotel_reviews, name='hotel_reviews'),
    path('agency/<int:agency_id>/reviews/', agency_reviews, name='agency_reviews'),
    path('hotels/<int:hotel_id>/', hotel_details, name='hotel_details'),
    path('agencies/<int:agency_id>/', agency_details, name='agency_details'),
    path('offers/', views.offers_view, name='offers'),
    path('offers/<int:offer_id>/', views.offer_detail, name='offer_detail'),
    
    
    
    
    
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)