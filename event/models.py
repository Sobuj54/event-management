from django.db import models
from category.models import Category
from django.contrib.auth import get_user_model

User = get_user_model()

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="events")
    participants = models.ManyToManyField(User, related_name="events", blank=True)
    image = models.ImageField(upload_to="event-images", blank=True, null=True)

    def __str__(self):
        return f"{self.name} on {self.date}"