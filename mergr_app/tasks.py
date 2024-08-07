## tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import User, Task
from datetime import datetime, timedelta

@shared_task
def send_notification_email(user_id: int, subject: str, message: str):
    """Send a notification email to a user."""
    try:
        user = User.objects.get(id=user_id)
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except User.DoesNotExist:
        pass

@shared_task
def check_task_deadlines():
    """Check for tasks that are nearing their deadlines and notify the assigned users."""
    now = datetime.now()
    upcoming_deadline = now + timedelta(days=1)
    tasks = Task.objects.filter(due_date__lte=upcoming_deadline, status='Pending')

    for task in tasks:
        subject = f"Task Deadline Approaching: {task.name}"
        message = f"Dear {task.assigned_to.username},\n\nThe task '{task.name}' is due on {task.due_date}. Please ensure it is completed on time.\n\nBest regards,\nYour Project Management Team"
        send_notification_email.delay(task.assigned_to.id, subject, message)
