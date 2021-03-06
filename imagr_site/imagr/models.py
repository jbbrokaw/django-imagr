import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser  # , UserManager

PUBLISHED_CHOICES = (
    ('private', 'This is private'),
    ('shared', 'This is shared'),
    ('public', 'This is public'),
)


# class ImagrUserManager(UserManager):
#     def create_user(username, email=None, password=None, **extra_fields):
#         user = ImagrUser(username=username, password=password, email=email)
#         return user

#     def create_superuser(username, email, password, **extra_fields):
#         user = ImagrUser(username=username, password=password, email=email,
#                          is_superuser=True)
#         return user


class ImagrUser(AbstractUser):
    following = models.ManyToManyField("self", related_name='followers',
                                       verbose_name='People I follow',
                                       blank=True,
                                       null=True,
                                       symmetrical=False)

    def followers_mask(self):
        return ", ".join(
            [follower.username for follower in self.followers.all()])
    followers_mask.short_description = "Followers"

    # objects = ImagrUserManager()


class Photo(models.Model):

    def __unicode__(self):
        return self.title

    title = models.CharField(max_length=140)
    description = models.CharField(max_length=2000, blank=True, null=True)
    date_uploaded = models.DateTimeField('date uploaded')
    date_modified = models.DateTimeField('date modified', blank=True,
                                         null=True)
    date_published = models.DateTimeField('date published', blank=True,
                                          null=True)
    published = models.CharField(max_length=8, choices=PUBLISHED_CHOICES)
    owner = models.ForeignKey(ImagrUser, verbose_name="Owner of photo",
                              related_name='photos')
    file_size = models.DecimalField(max_digits=6, decimal_places=3, blank=True,
                                    null=True, verbose_name="File Size (MB)")

    def was_published_recently(self):
        now = timezone.now()
        return (now - datetime.timedelta(days=5) <= self.date_published
                <= now)

    was_published_recently.boolean = True


class Album(models.Model):

    def __unicode__(self):
        return self.title

    # this refreshes the database each time if we default=now
    # now = timezone.now()
    date = datetime.date(2014, 11, 1)

    title = models.CharField(max_length=140)
    description = models.CharField(max_length=2000, blank=True, null=True)
    date_created = models.DateTimeField('date created', default=date)
    date_modified = models.DateTimeField('date modified', blank=True,
                                         null=True)
    date_published = models.DateTimeField('date published', blank=True,
                                          null=True)
    published = models.CharField(max_length=8, choices=PUBLISHED_CHOICES)
    owner = models.ForeignKey(ImagrUser, verbose_name="Owner of album")
    cover_photo = models.ForeignKey(Photo, related_name="cover_photo",
                                    blank=True, null=True)
    photos = models.ManyToManyField(Photo, verbose_name="photos in album",
                                    blank=True, null=True
                                    )
