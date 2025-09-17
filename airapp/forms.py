from django import forms
from .models import Book, Message


class BookingForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'email', 'nos']  # nos = number of tickets


class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'message']
