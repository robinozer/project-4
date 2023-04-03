"""
from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Reservation
from .forms import ReservationForm


@login_required
def reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'bookings/reservations.html', {'reservations': reservations})
"""


# View to display a specific table's details
class TableDetailView(DetailView):
    model = Table
    context_object_name = 'table'
    template_name = 'tables/table_detail.html'


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    # A view for displaying details of a single User object.
    model = User
    context_object_name = 'user'  # This is the name of the variable to be used in the template
    template_name = 'users/user_detail.html'  # The template used to render the view
    permission_required = ('users.view_user',)  # Permissions required to access the view


class BookingDetailView(LoginRequiredMixin, DetailView):
    # View for displaying details of a single booking
    model = Booking
    context_object_name = 'booking'
    template_name = 'bookings/booking_detail.html'