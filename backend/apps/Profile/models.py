from django.db import models
from apps.accounts.models import Account


class Skill(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Skills'

class Profile(models.Model):
    user        = models.OneToOneField(Account, on_delete=models.CASCADE)
    bio         = models.TextField(blank=True)
    avatar      = models.ImageField(upload_to='avatars/', blank=True, null=True)
    skills      = models.ManyToManyField(Skill, related_name='profiles', blank=True)

    def __str__(self):
        return self.user.email


class SocialLink(models.Model):
    owner       = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='social_links')

    facebook    = models.URLField(blank=True)    
    github      = models.URLField(blank=True)
    instagram   = models.URLField(blank=True)
    linkedin    = models.URLField(blank=True)
    reddit      = models.URLField(blank=True)

    telegram    = models.URLField(blank=True)
    twitch      = models.URLField(blank=True)
    tiktok      = models.URLField(blank=True)
    twitter     = models.URLField(blank=True)

    def __str__(self):
        return self.owner.email