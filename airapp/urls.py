from django.urls import path
from . import views

urlpatterns = [
    # --- Authentication ---
    path("", views.login_view, name="login"),  # Default landing page
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),

    # --- Home & Dashboard ---
    path("home/", views.home, name="home"),

    # --- Flight Search & Booking ---
    path("find_flight/", views.find_flight, name="find_flight"),
    path("bookings/", views.bookings, name="bookings"),
    path("mybookings/", views.seebookings, name="seebookings"),

    # --- Contact Form ---
    path("contact/", views.contact_us, name="contact_us"),
    path("contact_success/", views.contact_success, name="contact_success"),
]
