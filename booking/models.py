from django.db import models
from django.contrib.auth.models import User


class Table(models.Model):
    """A model representing a table in the restaurant."""
    number = models.IntegerField()  # The table number
    capacity = models.IntegerField()  # The maximum number of guests the table can seat

    def __str__(self):
        """Return a string representation of the table."""
        return f'Table {self.number} with capacity of {self.capacity} guests.'


class Booking(models.Model):
    """A model representing a booking made by a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who made the booking
    table = models.ForeignKey(Table, on_delete=models.CASCADE)  # The table reserved by the user
    date_time = models.DateTimeField()  # The date and time of the booking
    guests = models.IntegerField()  # The number of guests for the booking

    class Meta:
        ordering = ['-date_time']

    def __str__(self):
        """Return a string representation of the booking."""
        return f'{self.user.username} has booked - table no. {self.table} - {self.date_time}, for {self.guests} guests.'
