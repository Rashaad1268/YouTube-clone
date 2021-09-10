from django.contrib.auth.models import User
from django.db.models.signals import post_save

from base.models import CreatorProfile, Channel

def create_creator_profile(sender, instance, created, **kwargs):
    if created:
        creator_profile = CreatorProfile.objects.create(creator=instance)
        Channel.objects.create(owner=creator_profile)

        print("New CreatorProfile and Channel created!.")


post_save.connect(create_creator_profile, sender=User)