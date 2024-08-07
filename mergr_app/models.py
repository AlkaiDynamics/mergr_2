## models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class User(AbstractUser):
    """User model extending Django's AbstractUser."""
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username

class Profile(models.Model):
    """Profile model for storing additional user information."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    skills = models.JSONField(default=list)
    interests = models.JSONField(default=list)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Match(models.Model):
    """Match model for storing user matches."""
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user2')
    score = models.FloatField()

    def __str__(self):
        return f"Match between {self.user1.username} and {self.user2.username} with score {self.score}"

class Message(models.Model):
    """Message model for storing chat messages."""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.timestamp}"

class Project(models.Model):
    """Project model for storing project details."""
    name = models.CharField(max_length=255)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name='projects')

    def __str__(self):
        return self.name

class Task(models.Model):
    """Task model for storing task details."""
    name = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    due_date = models.DateTimeField()
    status = models.CharField(max_length=50, default='Pending')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.name
