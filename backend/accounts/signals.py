import secrets

from django.db.models.signals import post_save
from django.db.utils import IntegrityError
from django.dispatch import receiver

from accounts.models import User, Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        while 1:
            try:
                Profile.objects.create(user=instance, username='guest' + secrets.token_hex(8))
                break
            except IntegrityError:
                pass


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
