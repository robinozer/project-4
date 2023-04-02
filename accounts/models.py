from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    # Define a model that allows for custom user and superuser creation
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a new User with the given email and password.
        """
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

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a new superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Call create_user to create the new superuser
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    # Define fields for the User model
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
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
