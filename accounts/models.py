from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager


# Create and save a new User with the given email and password
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Email address is required")

        # Normalize the email address to lower case
        email = self.normalize_email(email)

        # Create a new User instance
        user = self.model(email=email)

        user.set_password(password)  # Hash the password before saving it
        user.save(using=self._db)  # Save the user to the database
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    # is_active is used to manage user account status and permissions in the app
    is_active = models.BooleanField(default=True)

    # Objects manager for User to handle user creation and management
    objects = UserManager()

    # Set the USERNAME_FIELD to email so that
    # users can log in with their email address
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # String representation of the User
    def __str__(self):
        return self.email


class Table(models.Model):
    table_number = models.IntegerField()
    capacity = models.IntegerField()  # Max no of guests the table can seat

    # String representation of the table.
    def __str__(self):
        return f'Table {self.table_number} with capacity of {self.capacity} guests.'


# Model representing a booking made by a user
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    guests = models.IntegerField()  # The number of guests for the booking

    class Meta:
        ordering = ['-date_time']

    # String representation of the booking.
    def __str__(self):
        return f'{self.user.username} - {self.date_time} for {self.guests} guests.'
