from django.db import models


class YoutubeCombined(models.Model):
    name = models.CharField(max_length=50)
    already_youtube_used = models.BooleanField(default=False)
    dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name