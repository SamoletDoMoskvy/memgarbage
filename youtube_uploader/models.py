from django.db import models
from video_downloader.models import Video


class Upload(models.Model):
    document = models.OneToOneField(Video,
                                    on_delete=models.CASCADE,
                                    related_name='uploads')

    dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



