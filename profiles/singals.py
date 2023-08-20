from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile, Setting

#registreren in de apps.py file van users!!!
@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        setting = Setting.objects.create()

        profile = Profile.objects.create(
            user = instance,
            setting=setting,
            username = instance.username,
            email = instance.email,
            name = instance.first_name
        )
       


@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    
    if created == False: #ortherwise a recursion error (infinit loop) user creats profile--> user-->profile-->...
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()




@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()
