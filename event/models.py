from django.shortcuts import get_object_or_404
from django.db import models
from django.contrib.auth.models import User
from user.models import UserProfile
from django.utils import timezone

# Create your models here.
class Event(models.Model):
    event_creator = models.ForeignKey(User, related_name="event_creator", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    information = models.CharField(max_length=350)
    header_image = models.ImageField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="event_participants", blank=True)
    event_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(blank=True, null=True, default=timezone.now)

    @classmethod
    def participant_accepted(cls, participant):
        cls.participants.add(participant)

    def __str__(self):
        return self.title
    
class EventInvite(models.Model):
    event = models.ForeignKey(Event, related_name="event_invite_event", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="event_invite_user", on_delete=models.CASCADE)
    created_date = models.DateTimeField(blank=True, null=True, default=timezone.now)

    @classmethod
    def create_invitation(cls, user, event):

        user_profile = get_object_or_404(UserProfile, user=user)
        user_profile.event_notification += 1
        user_profile.save()

        try:
            cls.objects.get(user=user, event=event)
        except:
            invitation = cls(
                event = event,
                user = user,
            )
            invitation.save()

    def __str__(self):
        return self.user.username
