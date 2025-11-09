from django.conf import settings
from django.db import models

from apps.jobs.models import Job

User = settings.AUTH_USER_MODEL


class Message(models.Model):
    """
    Represents a chat session between two users.

    Attributes:
        job (Job): The Job
        sender (User): The user who sent the message.
        receiver (User): The user who received the message.
        text (str): The content of the chat message.
        timestamp (datetime): When the message was sent.
        is_read (boolean): when msg read by reciever it will be true.
    """

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} ({self.timestamp})"
