from django.db import models
from django.contrib.auth.models import User


class Table(models.Model):
    """A model representing a table in the restaurant."""
    number = models.IntegerField()  # The table number
    capacity = models.IntegerField()  # The maximum number of guests the table can seat

    def __str__(self):
        """Return a string representation of the table."""
        return f'Table {self.number}'
