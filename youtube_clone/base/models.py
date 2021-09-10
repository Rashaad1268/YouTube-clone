from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    content = models.FileField(upload_to="videos/content/")
    thumbnail = models.ImageField(upload_to='images/thumbnails/')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=600)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='video_likes', default=None, blank=True)

    @property
    def total_likes(self):
        return self.likes.all().count()

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=60)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s | %s' % (self.video.title, self.commentator.username)


class CreatorProfile(models.Model):
    creator = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default="defaults/profile_pic.jpg", upload_to="images/profile_pics")
    bio = models.TextField(blank=True, null=True, max_length=350)

    def __str__(self):
        return str(self.creator)


SUBSCRIBE_CHOICES = (
    ('Subscribe', 'Subscribe'),
    ('Unubscribe', 'Unubscribe')
)

class Channel(models.Model):
    owner = models.ForeignKey(CreatorProfile, on_delete=models.CASCADE)
    subscriber = models.ManyToManyField(User, related_name='channel_subs', default=None, blank=True)

    def __str__(self):
        return f"Channel Owner: {self.owner}"

    @property
    def total_subscribers(self):
        return self.subscriber.all().count()


class Subscribe(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    value = models.CharField(choices=SUBSCRIBE_CHOICES, default='Subscribe', max_length=15)

    def __str__(self):
        return f"Channel: {self.channel.owner} | Subscribers: {self.channel.subscriber.all().count()}"


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return f"{self.user} | {self.video.title}"
