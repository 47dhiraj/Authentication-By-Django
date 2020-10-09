from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from pip._vendor import six

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.IntegerField(null=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)
    role = models.IntegerField(default=3)
    image = models.ImageField(upload_to='profile/', null=True, blank=True, default='profile/img_avatar.png')

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    ROLE_ADMIN = 1
    ROLE_TEACHER = 2
    ROLE_USER = 3


    # we will define signals so our Profile model will be automatically created/updated when we create/update User instances.
    # Basically we are hooking the create_user_profile and save_user_profile methods to the User model, whenever a save event occurs. This kind of signal is called post_save.

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()





class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.profile.email_confirmed)
        )

account_activation_token = AccountActivationTokenGenerator()