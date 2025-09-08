from django.db import models
from django.contrib.auth.models import AbstractUser
from users.utils import upi_validation


class User(AbstractUser):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    upi_id = models.CharField(
        max_length=255,
        blank=False,
        null=True,
        validators=[upi_validation],
        unique=True,
        help_text="UPI ID must be in the format of username@domain",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # password and password already exist in the User field, we're just using AbstractUser to modify a few fields of our choice as we deem fit
