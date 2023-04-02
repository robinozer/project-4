from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Reservation
from .forms import ReservationForm


@login_required
def reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'bookings/reservations.html', {'reservations': reservations})
