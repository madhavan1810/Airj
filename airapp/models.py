from django.db import models
from django.contrib.auth.models import User

# ------------------- FLIGHT MODEL -------------------

class Flight(models.Model):
    bus_name = models.CharField(max_length=100)  # Aircraft name or Airline name
    source = models.CharField(max_length=100)
    dest = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    nos = models.PositiveIntegerField()  # Total seats
    rem = models.PositiveIntegerField()  # Remaining seats
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Ticket price

    def __str__(self):
        return f"{self.bus_name} ({self.source} → {self.dest})"


# ------------------- BOOKING MODEL -------------------

class Book(models.Model):
    STATUS_CHOICES = [
        ('BOOKED', 'Booked'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    source = models.CharField(max_length=100)
    dest = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    nos = models.PositiveIntegerField()  # Number of seats booked
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='BOOKED')

    def __str__(self):
        return f"{self.name} - {self.flight.bus_name} ({self.date})"


# ------------------- CONTACT MESSAGE MODEL -------------------

class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
