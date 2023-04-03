from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import ListView, CreateView, UpdateView, DeleteView   # Is this one even necessary?
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages

from .models import Booking, User, Table


# List view to display all bookings made by a user.
class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'

    # Return the bookings for the currently logged in user.
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
