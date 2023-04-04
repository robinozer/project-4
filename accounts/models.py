from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Define a model that allows for custom user and superuser creation
class UserManager(BaseUserManager):
    # Create and save a new User with the given email and password.
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email address is required")

        # Normalize the email address to lower case
        email = self.normalize_email(email)

        # Create a new User instance with the given email and any extra fields
        user = self.model(email=email, **extra_fields)

        # Set the user's password using the set_password method, which
        # hashes the password before saving it
        user.set_password(password)

        # Save the user to the database using the database connection
        # used by the manager
        user.save(using=self._db)

        # Return the newly created user instance
        return user
    
    # Create and save a new superuser with the given email and password.
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Call create_user to create the new superuser
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    # Define fields for the User model
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    # is_active is used manage user account status and permissions in the app
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Define the objects manager for the User model
    # to handle user creation and management
    objects = UserManager()

    # Set the USERNAME_FIELD to email so that
    # users can log in with their email address
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Define a string representation for the User model
    def __str__(self):
        return self.email

    # Define a method to get the user's full name
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

    # Define a method to check if the user has a specific permission
    def has_perm(self, perm, obj=None):
        return True

    # Define a method to check if the user
    # has permissions for a specific module
    def has_module_perms(self, app_label):
        if app_label == 'auth':
            return self.is_superuser
        return True


class Table(models.Model):
    """A model representing a table in the restaurant,
    to keep track of available seating options."""
    table_number = models.IntegerField()  # The table number
    capacity = models.IntegerField()  # Max no of guests the table can seat

    def __str__(self):
        """Return a string representation of the table."""
        return f'Table {self.table_number} with capacity of {self.capacity} guests.'


class Booking(models.Model):
    """A model representing a booking made by a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who made the booking
    table = models.ForeignKey(Table, on_delete=models.CASCADE)  # The table reserved by the user
    date_time = models.DateTimeField()  # The date and time of the booking
    guests = models.IntegerField()  # The number of guests for the booking
    confirmed = models.BooleanField(default=False)  # Booking confirmation Y/N

    class Meta:
        ordering = ['-date_time']

    def __str__(self):
        """Return a string representation of the booking."""
        return f'{self.user.username} has booked - table no. {self.table} - {self.date_time}, for {self.guests} guests.'
