from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Flight, Book, Message
from .forms import ContactForm


# ---------------------- AUTHENTICATION ----------------------

def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            error = "Invalid username or password."
    return render(request, "login.html", {"error": error})


def logout_view(request):
    logout(request)
    return redirect("login")


def register_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            error = "Passwords do not match."
        elif User.objects.filter(username=username).exists():
            error = "Username already exists."
        elif User.objects.filter(email=email).exists():
            error = "Email is already registered."
        else:
            User.objects.create_user(username=username, email=email, password=password1)
            return redirect("login")

    return render(request, "register.html", {"error": error})


# ---------------------- HOME / DASHBOARD ----------------------

def home(request):
    return render(request, "home.html")


# ---------------------- FLIGHT SEARCH & BOOKING ----------------------

def find_flight(request):
    context = {}
    if request.method == "POST":
        source = request.POST.get('source')
        dest = request.POST.get('destination')
        date = request.POST.get('date')

        flight_list = Flight.objects.filter(source=source, dest=dest, date=date)

        if flight_list.exists():
            context.update({
                "flight_list": flight_list,
                "source": source,
                "dest": dest
            })
            return render(request, "list.html", context)  # ✅ Show results in list.html
        else:
            context["error"] = "No flights found for the selected route and date."

    return render(request, "find_flight.html", context)


@login_required(login_url='login')
def bookings(request):
    if request.method == 'POST':
        flight_id = request.POST.get("flight_id")
        tickets = request.POST.get("no_seats")

        try:
            tickets = int(tickets)
            flight = get_object_or_404(Flight, id=flight_id)

            if tickets <= 0:
                raise ValueError("Invalid number of seats.")

            if flight.rem >= tickets:
                total_cost = tickets * flight.price

                Book.objects.create(
                    user=request.user,
                    flight=flight,
                    name=request.user.username,
                    email=request.user.email,
                    source=flight.source,
                    dest=flight.dest,
                    price=flight.price,
                    nos=tickets,
                    date=flight.date,
                    time=flight.time,
                    status='BOOKED'
                )

                flight.rem -= tickets
                flight.save()

                return render(request, 'bookings.html', {
                    "flight": flight,
                    "tickets": tickets,
                    "total_cost": total_cost
                })
            else:
                return render(request, "find_flight.html", {
                    "error": f"Only {flight.rem} seat(s) available. Please reduce your booking count."
                })

        except (ValueError, Flight.DoesNotExist):
            return render(request, "find_flight.html", {
                "error": "Invalid booking request. Please try again."
            })

    return redirect("find_flight")


# ---------------------- FLIGHT BOOKING HISTORY ----------------------

@login_required(login_url='login')
def seebookings(request):
    bookings = Book.objects.filter(user=request.user)
    if bookings.exists():
        return render(request, "booklist.html", {"book_list": bookings})
    else:
        return render(request, "find_flight.html", {
            "error": "You haven't booked any flights yet."
        })


# ---------------------- CONTACT FORM ----------------------

def contact_us(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('contact_success')
    return render(request, 'contact.html', {"form": form})


def contact_success(request):
    return render(request, 'contact_success.html')
