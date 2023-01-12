from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, User


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    @receiver(post_save, sender=User)
    def user_profile(sender, instance, **kwargs):
        instance.user_profile.save()