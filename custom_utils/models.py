from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.utils.translation import ugettext_lazy as _


class CustomEmailUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')

        if not password:
            raise ValueError('The given password must be set')

        email = self.normalize_email(email)
        user = self.model(
        	email=email,
        	is_staff=is_staff,
        	is_active=True,
			is_superuser=is_superuser,
			date_joined=now,
			**extra_fields
		)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(
        	email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(
        	email, password, True, True, **extra_fields)

class CustomEmailUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomEmailUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
    	verbose_name = _("User")
    	verbose_name_plural = _("Users")

