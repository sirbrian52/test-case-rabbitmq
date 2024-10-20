from django.db import models
from django.contrib.auth.hashers import make_password

class employee(models.Model):
    name = models.CharField(max_length=100)
    badge = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=128) 

    def save(self, *args, **kwargs):
        if self.password:  
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
