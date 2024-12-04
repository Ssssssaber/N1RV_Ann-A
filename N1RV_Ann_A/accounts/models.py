from services.models import Hairdresser
from django.contrib.auth.models import AbstractUser
from django.db import models

# from django.contrib.auth import get_user_model
# User = get_user_model()

class UserAccount(AbstractUser):

    class Meta:
        abstract = False
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    hairdresser_preference = models.ManyToManyField(
        Hairdresser,
        verbose_name="Предпочтения по парикмахерам",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username

