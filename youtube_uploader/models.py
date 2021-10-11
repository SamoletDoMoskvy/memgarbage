from django.db import models
from video_combiner.models import Combined


class Video(models.Model):
    name = models.OneToOneField(Combined,
                                on_delete=models.CASCADE,
                                related_name='uploads')

    dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
