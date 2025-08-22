from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class MyUser(models.Model):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    ]
    
    SPECIALIZATION_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('anesthesiology', 'Anesthesiologist'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
    ]
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20,null=True)
    cpassword = models.CharField(max_length=20,null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES, blank=True, null=True)  
    is_approved = models.BooleanField(default=False) 
    is_available = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    fees = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name ({self.role})
    
    def clean(self):
        if self.role != 'doctor' and self.fees:
            raise ValidationError("Only doctors can have fees.")