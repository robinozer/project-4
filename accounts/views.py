from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import ListView, CreateView, UpdateView, DeleteView   # Is this one necessary?
from django.contrib.auth.decorators import login_required, permission_required      # Is this one also necessary?
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages

from .models import Booking, User, Table


# List view to display all bookings made by a user
class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 8

    # Return the bookings for the currently logged in user
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


# Display details of a single booking
class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'bookings'


# Create a new booking
class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    fields = ['table', 'date_time', 'guests']
    success_url = reverse_lazy('booking_list')
    template_name = 'bookings/booking_form.html'

    # Set the current user as the user for the new booking
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Update an existing booking
class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    fields = ['table', 'date_time', 'guests']
    success_url = reverse_lazy('booking_list')
    template_name = 'bookings/booking_form.html'


# Delete an existing booking
class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    success_url = reverse_lazy('booking_list')
    template_name = 'bookings/booking_confirm_delete.html'


#  Views for Table model


# Display all tables
class TableListView(ListView):
    model = Table
    context_object_name = 'table'
    template_name = 'tables/table_list.html'
    paginate_by = 8


# Display a specific table's details
class TableDetailView(DetailView):
    model = Table
    context_object_name = 'table'
    template_name = 'tables/table_detail.html'


# Create a new table
class TableCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Table
    fields = ['table_number', 'capacity']
    template_name = 'tables/table_form.html'
    permission_required = ('tables.add_table',)

    # Overriding the form_valid method to customize the success message
    def form_valid(self, form):
        table = form.save()
        messages.success(self.request, 'Table created successfully')
        return redirect('table-detail', pk=table.pk)


# Update an existing table
class TableUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Table
    fields = ['table_number', 'capacity']
    template_name = 'tables/table_form.html'
    permission_required = ('tables.change_table',)

    # Overriding the form_valid method to customize the success message
    def form_valid(self, form):
        table = form.save()
        messages.success(self.request, 'Table updated successfully')
        return redirect('table-detail', pk=table.pk)


# Delete an existing table
class TableDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Table
    context_object_name = 'table'
    template_name = 'tables/table_confirm_delete.html'
    success_url = reverse_lazy('table-list')
    permission_required = ('tables.delete_table',)
