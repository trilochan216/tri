from django.db import models
from django.contrib.auth.hashers import make_password

class Seller(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # Field to store hashed password
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if not self.pk:  # Only hash the password if it's a new instance
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
