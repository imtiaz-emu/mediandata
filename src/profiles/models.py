from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def upload_location(instance, filename):
	return "%s/%s/%s" % ('profile', instance.id, filename)


class Profile(models.Model):
	user = models.OneToOneField(
		User,
		on_delete=models.CASCADE
	)
	job_title = models.CharField(max_length=255, null=True)
	organization_name = models.CharField(max_length=255, null=True)
	phone_country_code = models.CharField(max_length=255, null=True)
	phone_number = models.CharField(max_length=255, null=True)
	description = models.TextField(blank=True, null=True)
	url = models.URLField(blank=True, null=True)
	address = models.CharField(max_length=255, null=True)
	photo = models.ImageField(upload_to=upload_location, default='media/No-img.jpg',
														max_length=None, null=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

	def get_full_name(self):
		""" Used to get a user full name"""
		return self.user.first_name + " " + self.user.last_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()
