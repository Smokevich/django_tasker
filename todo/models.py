from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    endtime = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name