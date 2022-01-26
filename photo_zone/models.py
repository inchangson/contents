from django.db import models


class Feed(models.Model):
    content = models.TextField()
    image = models.TextField()
    profile_image = models.TextField()
    username = models.TextField()
    # like_count = models.IntegerField()


class Reply(models.Model):
    feed_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    content = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['feed_id'])
        ]

class Like(models.Model):
    feed_id = models.IntegerField()
    username = models.CharField(max_length=30, blank=True, null=True)
    # is_like = models.BooleanField()
    # feed_id = models.IntegerField(default=0)
    # email = models.EmailField(default='')
    is_like = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['feed_id'])
        ]
    
