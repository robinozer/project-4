from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required  # Is this one necessary?
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages

from .models import Booking, Table, User


# Views for Bookings model


# List view to display all bookings made by a user
class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'index.html'  # The template used to render the view
    context_object_name = 'bookings'  # The name of the variable to be used in the template
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
    fields = ['table', 'date_time', 'guests']  # Fields to be included in the form
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
    context_object_name = 'tables'
    template_name = 'tables/table_list.html'
    paginate_by = 8


# Display a specific table's details
class TableDetailView(DetailView):
    model = Table
    context_object_name = 'table'
    template_name = 'tables/table_detail.html'


# Create a new table
class TableCreateView(LoginRequiredMixin, CreateView):
    model = Table
    fields = ['table_number', 'capacity']
    template_name = 'tables/table_form.html'

    # Overriding the form_valid method to customize the success message
    def form_valid(self, form):
        table = form.save()
        messages.success(self.request, 'Table created successfully')
        return redirect('table-detail', pk=table.pk)


# Update an existing table
class TableUpdateView(LoginRequiredMixin, UpdateView):
    model = Table
    fields = ['table_number', 'capacity']
    template_name = 'tables/table_form.html'

    # Overriding the form_valid method to customize the success message
    def form_valid(self, form):
        table = form.save()
        messages.success(self.request, 'Table updated successfully')
        return redirect('table-detail', pk=table.pk)


# Delete an existing table
class TableDeleteView(LoginRequiredMixin, DeleteView):
    model = Table
    context_object_name = 'table'
    template_name = 'tables/table_confirm_delete.html'
    success_url = reverse_lazy('table-list')


# Views for User model


# Display a list of all User objects
class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users/user_list.html'
    permission_required = ('users.view_user')
    paginate_by = 8


# Display the details of a single User
class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/user_detail.html'
    permission_required = ('users.view_user')


# Create a new User
class UserCreateView(CreateView):
    model = User
    fields = ['email', 'first_name', 'last_name', 'password']
    template_name = 'users/user_form.html'
    permission_required = ('users.add_user')

    # This method is called when valid form data has been POSTed.
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])  # Encrypt the user's password before saving
        user.save()
        messages.success(self.request, 'User created successfully')
        return redirect('user-detail', pk=user.pk)


