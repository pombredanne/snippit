from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom User Manager
    """

    def create_user(self, username, password, email, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, is_active=True, email=email,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email,  **extra_fields):
        return self.create_user(username=username, password=password,
                                email=email, **extra_fields)