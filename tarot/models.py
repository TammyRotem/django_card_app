from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
    

class Card(models.Model):
    card_name = models.TextField(null = True)
    card_element = models.TextField(null = True)
    card_suit = models.TextField(null = True)
    card_number = models.IntegerField(null = True)
    card_arcana_rank = models.TextField(null = True)
    card_astro_sign = models.TextField(null=True)
    card_astro_planet = models.TextField(null=True)
    card_key_term = models.TextField(null = True)
    card_image = models.ImageField(null=True,upload_to="tarot")

    def __str__(self):
        return str(self.card_name)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Reading(models.Model):
    num_of_cards = models.IntegerField(null = True)
    cards = models.ManyToManyField(Card)
    question = models.TextField(null = True)
    created_at = models.DateTimeField(null = True,auto_now_add=True)
    owner = models.ForeignKey(UserProfile, on_delete = models.CASCADE, null = True)

    def __str__(self):
        return str(self.question)













