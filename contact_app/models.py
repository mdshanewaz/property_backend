from django.db import models

# Create your models here.
class ContactModel(models.Model):

    firts_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15) 
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=300)
    message = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.last_name} - {self.subject}"