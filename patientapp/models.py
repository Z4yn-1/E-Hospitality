from django.db import models
from accounts.models import MyUser
# Create your models here.

class Appointment(models.Model):
    booked_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="booked_appointments")  # who logged in
    patient_name = models.CharField(max_length=100) 
    doctor = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="appointments_as_doctor")
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20,default="Pending")
    is_seen = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.patient_name} -> {self.doctor.name} on {self.date}"
