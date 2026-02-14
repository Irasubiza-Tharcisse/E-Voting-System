from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Define user roles
    ROLE_CHOICES = (
        ('voter', 'Voter'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='voter')

    def is_voter(self):
        return self.role == 'voter'

    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return f"{self.username} ({self.role})"
    is_approved = models.BooleanField(default=False) # Add this line